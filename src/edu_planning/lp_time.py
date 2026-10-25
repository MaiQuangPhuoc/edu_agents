import re
from src.edu_planning.chapter_utils import normalize_chapter_id

_ROW = re.compile(r"\|\s*[\w.]+\s*\|\s*([^|]+?)\s*\|[^|]*\|\s*(\d+)\s*\|")
_MIN = re.compile(r"mỗi buổi\s*(\d+)\s*phút", re.I)


def chapter_plan_time(retriever, subject: str, chapter_id: str):
    """Đọc bảng 'Danh sách bài học' của giáo án: số buổi mỗi bài và phút/buổi. Không có giáo án thì trả None."""
    try:
        docs = retriever.lesson_plan_search(subject, chapter_id, limit=1, section_types=("lesson_list",))
    except Exception as e:
        print(f"[lp_time] lỗi {subject} chương {chapter_id}: {type(e).__name__} {str(e)[:100]}")
        return None
    if not docs:
        return None
    text = docs[0].page_content
    rows = [(m.group(1), int(m.group(2))) for m in _ROW.finditer(text)]
    m = _MIN.search(text)
    return {"minutes": int(m.group(1)) if m else 45, "lessons": rows} if rows else None


def time_facts_text(retriever, subject: str, phases: list, weeks: int, per_week: int, minutes: int) -> str:
    """Số liệu để LLM so khớp: thời lượng giáo án đề xuất và thời gian học sinh thực có (chỉ nêu số, không quyết định)."""
    lines, need = ["Thời lượng giáo án đề xuất (tự học):"], 0
    for p in phases:
        for c in p.get("chapters", []):
            cid = normalize_chapter_id(subject, c["chapter_id"]) or str(c["chapter_id"])
            info = chapter_plan_time(retriever, subject, cid)
            if not info:
                lines.append(f"- Chương {cid}: chưa có giáo án, tự cân đối theo số bài")
                continue
            total = sum(s for _, s in info["lessons"]) * info["minutes"]
            need += total
            lines.append(f"- Chương {cid}: {total} phút = " + "; ".join(
                f"{n} {s} buổi x {info['minutes']} phút" for n, s in info["lessons"]))
    cap = weeks * per_week * minutes
    lines += ["", f"Thời gian học sinh có: {weeks} tuần x {per_week} buổi x {minutes} phút = {cap} phút ({per_week * minutes} phút/tuần)"]
    if need:
        lines.append(f"Tổng thời lượng giáo án đề xuất (các chương có giáo án): {need} phút = {need / cap:.0%} thời gian học sinh có")
    return "\n".join(lines)