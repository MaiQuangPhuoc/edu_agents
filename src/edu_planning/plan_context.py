import sys, os, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import date
from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_planning.lp_tools import _deadline, _pick_goal

OVERVIEW_K = 3
OVERVIEW_MIN = 0.7          # xác suất sau sigmoid
OVERVIEW_FETCH = 15
OVERVIEW_MAX_CHARS = 700
OVERVIEW_SUBTYPE = {"Toán 10": "chapter"}      # môn nào có chunk tổng quan gắn sub_type; môn khác không lọc

GIAO_AN_MAX_CHARS = 1200
NEUTRAL = 0.6    
_UU_TIEN = {"diem_so": "ưu tiên điểm số", "hieu_ban_chat": "ưu tiên hiểu bản chất", "ca_hai": "cân bằng điểm số và hiểu bản chất"}

def _one(x) -> dict:
    if isinstance(x, dict):
        return x
    return x[0] if isinstance(x, list) and x else {}


def _subjects(sm: dict) -> list:
    items = (sm.get("nang_luc") or []) + (sm.get("muc_tieu") or [])
    return sorted({x["mon_hoc"] for x in items if x.get("mon_hoc")})


def _join(v) -> str:
    return "; ".join(map(str, v)) if isinstance(v, list) else str(v)


def time_text(sm: dict, today: date | None = None) -> str:
    today = today or date.today()
    per_week = _one(sm.get("lich_hoc")).get("so_buoi_tuan")
    minutes = _one(sm.get("so_thich_hoc")).get("thoi_luong_buoi_phut")
    lines = [f"Hôm nay: {today.isoformat()}"]
    for s in _subjects(sm):
        goal = _pick_goal(sm, s)
        if goal.get("mon_hoc") != s:
            goal = {}
        end, weeks = _deadline(goal, today)
        if not weeks:
            lines.append(f"- {s}: chưa rõ thời hạn")
            continue
        line = f"- {s}: còn {weeks} tuần (đến {end.isoformat()})"
        if per_week and minutes:
            sessions = int(per_week) * weeks
            line += f"; {per_week} buổi/tuần x {minutes} phút => tối đa {sessions} buổi, {sessions * int(minutes)} phút"
        else:
            line += "; chưa rõ số buổi/tuần hoặc thời lượng buổi"
        lines.append(line)
    return "\n".join(lines)


def _level(m: float) -> str:
    return "Mạnh" if m >= 0.7 else "Yếu" if m < 0.5 else "Trung bình"


def levels_text(sm: dict, batch: dict | None = None) -> str:
    lines = []
    for nl in sm.get("nang_luc") or []:
        s = nl.get("mon_hoc")
        if batch and s != batch["subject"]:
            continue
        topics = [t for t in nl.get("chu_de") or [] if t.get("muc_nam") is not None
                  and (not batch or str(t.get("chapter_id")) in batch["chapters"])]
        for t in sorted(topics, key=lambda t: t["muc_nam"]):
            lines.append(f"- {s} chương {t.get('chapter_id')}: {_level(t['muc_nam'])} "
                         f"(muc_nam={t['muc_nam']:.2f}, do_tin_cay={t.get('do_tin_cay')}, nguon={t.get('nguon')})")
        if nl.get("diem_yeu"):
            lines.append(f"- {s}: học sinh tự nêu điểm yếu: {_join(nl['diem_yeu'])}")
        if nl.get("diem_manh"):
            lines.append(f"- {s}: học sinh tự nêu điểm mạnh: {_join(nl['diem_manh'])}")
    return "\n".join(lines) or "(chưa có kết quả bài kiểm tra)"


def lesson_plan_text(retriever, sm: dict, batch: dict | None = None) -> str:
    pairs = ([(batch["subject"], c) for c in batch["chapters"]] if batch
             else [(s, c) for s in _subjects(sm) for c in get_subject_curriculum(s)])
    lines = []
    for s, ch_id in pairs:
        try:
            docs = retriever.lesson_plan_search(s, ch_id)
        except Exception as e:
            print(f"[giáo án] lỗi {s} chương {ch_id}: {str(getattr(e, 'content', e))[:300]}")
            lines.append(f"- {s} chương {ch_id}: không tra được giáo án")
            continue
        if not docs:
            lines.append(f"- {s} chương {ch_id}: chưa có giáo án")
            continue
        md = docs[0].metadata
        n, m = md.get("suggested_sessions"), md.get("minutes_per_session")
        tong = f"{n} buổi x {m} phút = {n * m} phút" if n and m else "chưa rõ số buổi/thời lượng"
        body = "\n".join(d.page_content[:GIAO_AN_MAX_CHARS] for d in docs)
        lines.append(f"- {s} chương {ch_id} | giáo án gợi ý: {tong} | "
                     f"trạng thái: {md.get('verification_status', 'không rõ')}\n{body}")
    return "\n".join(lines) or "(không có giáo án)"


def make_batches(sm: dict, size: int = 2) -> list[dict]:
    """Chia chương thành lô `size` chương theo từng môn; chương yếu (muc_nam thấp) đứng trước."""
    levels = {}
    for nl in sm.get("nang_luc") or []:
        for t in nl.get("chu_de") or []:
            if t.get("muc_nam") is not None:
                levels[(nl.get("mon_hoc"), str(t.get("chapter_id")))] = t["muc_nam"]
    out = []
    for s in _subjects(sm):
        ids = sorted(get_subject_curriculum(s), key=lambda c: levels.get((s, c), NEUTRAL))   # sort ổn định
        out += [{"subject": s, "chapters": ids[i:i + size]} for i in range(0, len(ids), size)]
    return out

def _yn(v) -> str:
    return "chưa rõ" if v is None else "có" if v else "không"


def profile_text(sm: dict) -> str:
    """Hồ sơ dạng ngôn ngữ tự nhiên, chỉ giữ thông tin cần cho việc lập sườn."""
    cn = sm.get("ca_nhan") or {}
    lines = [f"- Học sinh lớp {cn.get('khoi_lop', 10)}."]
    if cn.get("hoat_dong_ngoai_khoa"):
        lines.append(f"- Hoạt động ngoài giờ: {_join(cn['hoat_dong_ngoai_khoa'])}.")
    for nl in sm.get("nang_luc") or []:
        parts = []
        if nl.get("diem_hien_tai") is not None:
            parts.append(f"điểm hiện tại {nl['diem_hien_tai']}")
        if nl.get("diem_yeu"):
            parts.append(f"tự nhận yếu: {_join(nl['diem_yeu'])}")
        if nl.get("diem_manh"):
            parts.append(f"tự nhận mạnh: {_join(nl['diem_manh'])}")
        lines.append(f"- {nl.get('mon_hoc')}: " + ("; ".join(parts) or "chưa có thông tin năng lực") + ".")
    for g in sm.get("muc_tieu") or []:
        parts = []
        if g.get("muc_tieu_diem") is not None:
            parts.append(f"mục tiêu {g['muc_tieu_diem']} điểm")
        if g.get("han_chot"):
            parts.append(f"hạn chót: {g['han_chot']}")
        if g.get("ngay_ket_thuc"):
            parts.append(f"đến ngày {g['ngay_ket_thuc']}")
        elif g.get("so_tuan_con_lai"):
            parts.append(f"còn khoảng {g['so_tuan_con_lai']} tuần")
        if g.get("uu_tien"):
            parts.append(_UU_TIEN.get(g["uu_tien"], g["uu_tien"]))
        if g.get("dang_bai_can_giu"):
            parts.append(f"muốn tập trung dạng: {_join(g['dang_bai_can_giu'])}")
        lines.append(f"- Mục tiêu {g.get('mon_hoc')}: " + ("; ".join(parts) or "chưa rõ") + ".")
    st = _one(sm.get("so_thich_hoc"))
    lines.append(f"- Cách học: dùng video: {_yn(st.get('dung_video'))}; dùng tài liệu: {_yn(st.get('dung_tai_lieu'))}.")
    return "\n".join(lines)

def _prob(score: float) -> float:
    return float(score)      # bge-reranker-v2-m3 đã trả 0..1


def sgk_overview_text(retriever, batch: dict) -> str:
    """SGK tổng quan mỗi chương: query dựng bằng code, lọc subject+chapter_id, rerank, giữ tối đa 3 chunk có điểm > 0.7."""
    s = batch["subject"]
    cur = get_subject_curriculum(s)
    lines = []
    for ch_id in batch["chapters"]:
        name = cur.get(ch_id, {}).get("chapter_name", "")
        query = f"{name}: mục tiêu, khái quát toàn chương và giới thiệu chương"
        try:
            docs = retriever.search_sgk(query, s, ch_id, k=OVERVIEW_FETCH, sub_type=OVERVIEW_SUBTYPE.get(s))
            ranked = retriever.rerank(query, docs, top_k=OVERVIEW_K)
        except Exception as e:
            print(f"[SGK tổng quan] lỗi {s} chương {ch_id}: {type(e).__name__} {str(e)[:150]}")
            ranked = []
        probs = [_prob(d.metadata["rerank_score"]) for d in ranked]
        print(f"[SGK tổng quan] {s} chương {ch_id} | sub_type={OVERVIEW_SUBTYPE.get(s)} | query: {query} | điểm: {[round(p, 2) for p in probs]}")
        keep = [(p, d) for p, d in zip(probs, ranked) if p > OVERVIEW_MIN]
        if not keep:
            lines.append(f"- {s} chương {ch_id} ({name}): chưa có đoạn SGK tổng quan đủ liên quan")
            continue
        lines.append(f"- {s} chương {ch_id} ({name}):")
        lines += [f"  [{p:.2f}] {d.page_content[:OVERVIEW_MAX_CHARS]}" for p, d in keep]
    return "\n".join(lines)