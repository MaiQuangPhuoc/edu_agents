import json, math, re, unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path
import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.edu_planning.chapter_utils import normalize_chapter_id
from langchain_core.tools import tool
from src.edu_exam.curriculum import get_subject_curriculum

CACHE_DIR = Path("data/cache/chapter_knowledge")    # đổi theo cấu trúc dự án
DEFAULT_TARGET_SCORE = 7

# Cùng bảng với DIFFICULTY_RATIO trong build_matrix_v2.py: (easy, medium, hard)
_DIFFICULTY_RATIO = {
    5: (0.70, 0.25, 0.05), 6: (0.50, 0.35, 0.15), 7: (0.50, 0.35, 0.15),
    8: (0.35, 0.40, 0.25), 9: (0.20, 0.30, 0.50), 10: (0.20, 0.30, 0.50),
}

_RANGE = re.compile(r"(\d{1,2})(?:[:h](\d{2})?)?\s*(?:-|–|đến|den|to)\s*(\d{1,2})(?:[:h](\d{2})?)?", re.I)
_EN_DAYS = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}


# ───────────────────────── Cache ─────────────────────────

def _cache_path(subject: str, chapter_id: str) -> Path:
    slug = re.sub(r"\W+", "_", subject)
    return CACHE_DIR / f"{slug}_{chapter_id}.json"


def _load_cache(subject: str, chapter_id: str):
    path = _cache_path(subject, chapter_id)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _save_cache(subject: str, chapter_id: str, data: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _cache_path(subject, chapter_id).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ───────────────────────── Phân tích kiến thức chương ─────────────────────────

def _analyze(retriever, llm_client, subject: str, chapter_id: str) -> dict:
    cur = get_subject_curriculum(subject)
    chapter_id = normalize_chapter_id(subject, chapter_id) or chapter_id
    chapter = cur.get(chapter_id)
    if not chapter:
        return {"error": f"Không có chương {chapter_id} trong {subject}"}

    cached = _load_cache(subject, chapter_id)
    if cached:
        return cached

    from src.edu_planning.lp_knowledge import analyze_chapter     # import trong hàm để tránh vòng import
    data, failed = analyze_chapter(retriever, llm_client, subject, chapter_id)
    if len(failed) == len(data["lessons"]) or not any(ls["key_points"] for ls in data["lessons"]):
        return {"error": f"Không phân tích được chương {chapter_id}"}
    if failed:                                  # lỗi một phần: trả kết quả nhưng không cache để lần sau thử lại
        data["failed_lessons"] = failed
        return data
    _save_cache(subject, chapter_id, data)
    return data


# ───────────────────────── Quy hoạch thời gian ─────────────────────────

def _norm(s: str) -> str:
    s = s.lower().replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def _weekday(key: str):
    """Thứ 2..CN hoặc tên tiếng Anh -> 0..6 (Mon..Sun); None nếu không hiểu."""
    k = _norm(key)
    m = re.search(r"[2-7]", k)
    if "thu" in k and m:
        return int(m.group()) - 2
    if "chu nhat" in k or k in ("cn", "sun", "sunday"):
        return 6
    for name, idx in _EN_DAYS.items():
        if k.startswith(name):
            return idx
    return None


def _parse_free_time(free: dict, warnings: list) -> dict:
    out = {}
    for key, ranges in (free or {}).items():
        wd = _weekday(str(key))
        if wd is None:
            warnings.append(f"Không hiểu ngày '{key}' trong khung giờ rảnh")
            continue
        for text in (ranges if isinstance(ranges, list) else [ranges]):
            m = _RANGE.search(str(text))
            if not m:
                warnings.append(f"Không hiểu khung giờ '{text}' ({key})")
                continue
            s = int(m.group(1)) * 60 + int(m.group(2) or 0)
            e = int(m.group(3)) * 60 + int(m.group(4) or 0)
            if e > s:
                out.setdefault(wd, []).append((s, e))
    return out


def _pick_goal(sm: dict, subject: str) -> dict:
    goals = sm.get("muc_tieu") or []
    return next((g for g in goals if g.get("mon_hoc") == subject), goals[0] if goals else {})


def _deadline(goal: dict, start: date):
    end = goal.get("ngay_ket_thuc")
    if end:
        try:
            d = date.fromisoformat(end)
            return d, max(1, math.ceil((d - start).days / 7))
        except ValueError:
            pass
    weeks = goal.get("so_tuan_con_lai")
    if weeks:
        return start + timedelta(weeks=int(weeks)), int(weeks)
    return None, None


def _week_sessions(free: dict, block_start: date, per_week: int, minutes: int, now: datetime) -> list:
    """Chọn per_week buổi trong khối 7 ngày. Ưu tiên mỗi ngày một buổi, rải đều; thiếu thì xếp thêm buổi
    liền sau trong cùng khung rảnh (khung dài đủ nhiều buổi). Hôm nay: chỉ dùng phần khung còn lại."""
    days = []                                              # [(ngày, [giờ bắt đầu các buổi có thể xếp])]
    for i in range(7):
        d = block_start + timedelta(days=i)
        starts = []
        for s, e in sorted(free.get(d.weekday(), [])):
            if d == now.date():
                s = max(s, -(-(now.hour * 60 + now.minute) // 5) * 5)    # làm tròn lên 5 phút
            while e - s >= minutes:
                starts.append(s)
                s += minutes
        if starts:
            days.append((d, starts))
    if not days:
        return []
    n, k = len(days), min(per_week, len(days))
    pick = [0] if k == 1 else sorted({round(i * (n - 1) / (k - 1)) for i in range(k)})
    chosen = [(days[i][0], days[i][1][0]) for i in pick]               # vòng 1: mỗi ngày một buổi
    extra = [(d, s) for d, st in days for s in st[1:]]                 # vòng 2: buổi thêm trong ngày
    extra.sort(key=lambda x: (x[0] not in {c[0] for c in chosen}, x[0], x[1]))
    chosen = sorted(chosen + extra[:max(0, per_week - len(chosen))])
    return [{"date": d.isoformat(), "start_time": f"{s // 60:02d}:{s % 60:02d}", "minutes": minutes} for d, s in chosen]


def _build_schedule(sm: dict, subject: str, window: dict) -> dict:
    if window.get("slots"):                      # lịch đã đóng băng ở plan_node
        return window["slots"]
    
    lich, sthich = sm.get("lich_hoc") or {}, sm.get("so_thich_hoc") or {}
    per_week, minutes = lich.get("so_buoi_tuan"), sthich.get("thoi_luong_buoi_phut")
    missing = [n for n, v in [("so_buoi_tuan", per_week), ("thoi_luong_buoi_phut", minutes),
                              ("khung_gio_ranh", lich.get("khung_gio_ranh"))] if not v]
    if missing:
        return {"error": f"Hồ sơ thiếu: {', '.join(missing)}"}

    warnings = []
    free = _parse_free_time(lich["khung_gio_ranh"], warnings)
    now = datetime.now()
    try:
        start = date.fromisoformat(window["start_date"]) if window.get("start_date") else now.date()
    except ValueError:
        return {"error": f"start_date không hợp lệ: {window.get('start_date')}"}

    num_weeks, first = int(window.get("num_weeks", 1)), int(window.get("first_week_no", 1))
    deadline, weeks_remaining = _deadline(_pick_goal(sm, subject), start)

    weeks, total = [], 0
    for i in range(num_weeks):
        block = start + timedelta(days=7 * i)
        sessions = _week_sessions(free, block, int(per_week), int(minutes), now)
        if len(sessions) < int(per_week):
            warnings.append(f"Tuần {first + i}: chỉ xếp được {len(sessions)}/{per_week} buổi theo khung giờ rảnh")
        total += len(sessions)
        weeks.append({"week_no": first + i, "start_date": block.isoformat(),
                      "end_date": (block + timedelta(days=6)).isoformat(), "sessions": sessions})

    if deadline and start + timedelta(days=7 * num_weeks - 1) > deadline:
        warnings.append(f"Cửa sổ vượt quá thời hạn ({deadline.isoformat()})")
    if lich.get("lich_ban"):
        warnings.append("Lịch bận (chưa được kiểm tra tự động): " + "; ".join(map(str, lich["lich_ban"])))

    return {
        "start_date": start.isoformat(), "deadline": deadline.isoformat() if deadline else None,
        "weeks_remaining": weeks_remaining, "sessions_per_week": int(per_week),
        "minutes_per_session": int(minutes), "weeks": weeks, "total_sessions": total,
        "total_hours": round(total * int(minutes) / 60, 2), "warnings": warnings,
    }


def _chapter_sizes(subject: str, chapter_ids: list) -> dict:
    cur = get_subject_curriculum(subject)
    return {c: sum(len(v) for v in cur[c]["lessons"].values()) for c in chapter_ids if c in cur}


def _allocate(total: int, sizes: dict) -> dict:
    """Chia total buổi theo tỉ lệ kích thước chương (phần dư chia theo phần thập phân lớn nhất)."""
    tot = sum(sizes.values()) or 1
    raw = {c: total * s / tot for c, s in sizes.items()}
    base = {c: int(v) for c, v in raw.items()}
    rest = total - sum(base.values())
    for c in sorted(raw, key=lambda c: raw[c] - base[c], reverse=True)[:rest]:
        base[c] += 1
    return base


# ───────────────────────── Factory ─────────────────────────

def make_lp_tools(retriever, llm_client, student_model: dict, subject: str, window: dict):
    """window = {"start_date": "YYYY-MM-DD" | None, "num_weeks": 1, "first_week_no": 1, "chapter_ids": ["1", "2"]}
    Tạo mới cho mỗi lần chạy vì hồ sơ, môn và cửa sổ khác nhau giữa các lần."""

    @tool
    def analyze_chapter_knowledge(chapter_id: str) -> str:
        """Phân tích kiến thức của MỘT chương: với mỗi bài có ý chính, cần nắm, cần hiểu, dạng bài và liên hệ với bài khác.

        Dùng khi:
        - Cần biết nội dung kiến thức của chương để soạn buổi học.
        - Cần quan hệ giữa các bài, các dạng bài.

        Kết quả được lưu cache theo chương nên gọi lại rất nhanh. Mỗi lần gọi một chương.

        Args:
            chapter_id: số chương dạng chuỗi, ví dụ "I" (Toán) hoặc "5" (Ngữ văn, Lịch sử).
        """
        return json.dumps(_analyze(retriever, llm_client, subject, str(chapter_id)), ensure_ascii=False)

    @tool
    def compute_schedule() -> str:
        """Tính các buổi học cụ thể (ngày, giờ bắt đầu, thời lượng) trong cửa sổ hiện tại từ lịch học của học sinh.

        Dùng khi:
        - Cần biết có mấy buổi, vào ngày giờ nào, mỗi buổi bao lâu.
        - Cần biết còn bao nhiêu tuần đến thời hạn.

        Không cần tham số. Kết quả gồm danh sách buổi theo tuần, tổng số buổi, tổng giờ, gợi ý số buổi cho mỗi chương
        (chia theo kích thước chương; bạn có thể điều chỉnh theo điểm yếu của học sinh) và cảnh báo nếu có.
        """
        res = _build_schedule(student_model, subject, window)
        if "error" not in res:
            sizes = _chapter_sizes(subject, window.get("chapter_ids") or [])
            if sizes:
                res["chapter_sizes"] = sizes
                res["suggested_sessions_per_chapter"] = _allocate(res["total_sessions"], sizes)
        return json.dumps(res, ensure_ascii=False)

    @tool
    def compute_difficulty_ratio() -> str:
        """Tính tỉ lệ độ khó (easy, medium, hard) theo điểm mục tiêu của học sinh, và số buổi mỗi mức trong cửa sổ.

        Dùng khi:
        - Cần quyết định độ khó cho các buổi học trong cửa sổ.

        Không cần tham số. Việc chương nào dễ trước khó sau do bạn quyết định dựa trên kết quả này.
        """
        goal = _pick_goal(student_model, subject)
        score, notes = goal.get("muc_tieu_diem"), []
        if score is None:
            score = DEFAULT_TARGET_SCORE
            notes.append(f"Hồ sơ chưa có điểm mục tiêu, tạm dùng {DEFAULT_TARGET_SCORE}")
        e, m, h = _DIFFICULTY_RATIO[min(max(int(round(score)), 5), 10)]
        res = {"target_score": score, "ratio": {"easy": e, "medium": m, "hard": h}, "notes": notes}

        sched = _build_schedule(student_model, subject, window)
        if "error" not in sched:
            n = sched["total_sessions"]
            easy, hard = round(n * e), round(n * h)
            res["sessions"] = n
            res["session_counts"] = {"easy": easy, "medium": max(n - easy - hard, 0), "hard": hard}
        return json.dumps(res, ensure_ascii=False)

    return [analyze_chapter_knowledge, compute_schedule, compute_difficulty_ratio]