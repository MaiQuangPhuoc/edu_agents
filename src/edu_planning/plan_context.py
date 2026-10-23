import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import date
from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_planning.lp_tools import _deadline, _pick_goal

GIAO_AN_MAX_CHARS = 1200
NEUTRAL = 0.6    

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