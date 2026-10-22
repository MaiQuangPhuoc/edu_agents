"""Tạo search_queries bằng code (không dùng LLM): chương yếu tách riêng, chương còn lại gộp một query."""
from src.edu_exam.curriculum import CURRICULUM

MAX_QUERIES = 6
MAX_VIDEOS = 2


def _subject(model: dict) -> str | None:
    for x in (model.get("nang_luc") or []) + (model.get("muc_tieu") or []):
        n = (x.get("mon_hoc") or "").strip().lower()
        s = next((k for k in CURRICULUM if n and k.lower().startswith(n)), None)
        if s:
            return s
    return None


def _q(query: str, subject: str, chapter_id, nguon: str = "sgk") -> dict:
    return {"query": query, "subject": subject, "chapter_id": chapter_id, "nguon": nguon}


def build_queries(model: dict) -> list[dict]:
    subject = _subject(model)
    if not subject:
        return []
    chapters = CURRICULUM[subject]
    nl = next((x for x in model.get("nang_luc") or [] if x.get("mon_hoc", "").lower() in subject.lower()), {})
    ratio = {c["chapter_id"]: c.get("muc_nam") for c in nl.get("chu_de") or []}
    weak = [c for c in nl.get("diem_yeu") or [] if c in chapters]
    weak.sort(key=lambda c: 1.0 if ratio.get(c) is None else ratio[c])           # yếu nhất trước
    rest = [c for c in list(chapters) if c not in weak and (c in (nl.get("diem_manh") or []) or c in ratio)]

    out = [_q(f"{chapters[c]['chapter_name']}: " + "; ".join(chapters[c]["lessons"]), subject, c) for c in weak]
    if rest:                                                                         # chương còn lại: một query gộp
        names = "; ".join(chapters[c]["chapter_name"] for c in rest)
        out.append(_q(f"ôn tập {names}", subject, rest[0] if len(rest) == 1 else None))
    if (model.get("so_thich_hoc") or {}).get("dung_video"):
        out += [_q(f"video bài giảng {chapters[c]['chapter_name']}", subject, c, "video") for c in weak[:MAX_VIDEOS]]
    return out[:MAX_QUERIES]