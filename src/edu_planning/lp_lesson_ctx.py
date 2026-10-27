import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_planning.plan_context import sgk_overview_text, NO_RERANK

GA_MAX_CHARS = 1500       # tối đa mỗi chunk giáo án đưa vào prompt
SGK_PER_LESSON = 3        # số chunk SGK giữ cho mỗi bài
SGK_FETCH = 12            # số chunk lấy về trước khi rerank
SGK_MAX_CHARS = 700

def _norm(s: str) -> str:
    """Chữ thường, bỏ tiền tố "Bài 1." và dấu câu để so tên bài."""
    s = re.sub(r"^\s*bài\s*\d+\s*[.:\-–]?\s*", "", str(s).lower())
    return " ".join(re.sub(r"[^\w\s]", " ", s).split())


def _match(lesson: str, titles: list) -> str | None:
    """Tên bài trong chương trình -> lesson_title trong giáo án: chỉ khớp đúng sau khi chuẩn hóa
    (không khớp "chứa nhau" vì "Tập hợp" sẽ khớp nhầm "Các phép toán trên tập hợp")."""
    n = _norm(lesson)
    return next((t for t in titles if _norm(t) == n), None)


def _lesson_plan_ctx(retriever, subject: str, chapter_id: str, lessons: list) -> dict:
    try:
        by_title = retriever.lesson_plan_lessons(subject, chapter_id)
    except Exception as e:
        print(f"[ctx] lỗi giáo án {subject} chương {chapter_id}: {type(e).__name__} {str(e)[:150]}")
        return {}
    out = {}
    for name in lessons:
        title = _match(name, list(by_title))
        if title:
            out[name] = "\n".join(d.page_content[:GA_MAX_CHARS] for d in by_title[title])
    return out


def _sgk_ctx(retriever, subject: str, chapter_id: str, chapter: dict, names: list) -> dict:
    use_rerank = subject not in NO_RERANK
    queries, docs_list = [], []
    for name in names:
        secs = [s for s in chapter["lessons"][name] if s != name][:4]
        q = f"{chapter['chapter_name']} {name} {'; '.join(secs)}".strip()
        try:
            docs = retriever.search_sgk(q, subject, chapter_id, k=SGK_FETCH if use_rerank else SGK_PER_LESSON)
        except Exception as e:
            print(f"[ctx] lỗi SGK {subject} chương {chapter_id} bài {name}: {type(e).__name__} {str(e)[:150]}")
            docs = []
        queries.append(q)
        docs_list.append(docs)
    if use_rerank:
        docs_list = retriever.rerank_batch(queries, docs_list, top_k=SGK_PER_LESSON)
    return {n: "\n".join(f"- {d.page_content[:SGK_MAX_CHARS]}" for d in docs)
            for n, docs in zip(names, docs_list) if docs}


def chapter_contexts(retriever, subject: str, chapter_id: str) -> dict:
    """Ngữ cảnh từng bài của một chương: ưu tiên giáo án; bài nào không có giáo án thì dùng SGK.
    Trả {"overview": str, "lessons": {tên bài: {"source": "lesson_plan"|"sgk"|"none", "text": str}}}.
    overview (SGK tổng quan chương) chỉ có khi còn bài phải dùng SGK."""
    chapter = get_subject_curriculum(subject).get(chapter_id)
    if not chapter:
        return {"overview": "", "lessons": {}}
    names = list(chapter["lessons"])
    plan = _lesson_plan_ctx(retriever, subject, chapter_id, names)
    missing = [n for n in names if n not in plan]
    sgk, overview = {}, ""
    if missing:
        sgk = _sgk_ctx(retriever, subject, chapter_id, chapter, missing)
        overview = sgk_overview_text(retriever, {"subject": subject, "chapters": [chapter_id]}, verbose=False)
    lessons = {}
    for n in names:
        if n in plan:
            lessons[n] = {"source": "lesson_plan", "text": plan[n]}
        elif n in sgk:
            lessons[n] = {"source": "sgk", "text": sgk[n]}
        else:
            lessons[n] = {"source": "none", "text": ""}
    return {"overview": overview, "lessons": lessons}


def sgk_extra(retriever, subject: str, chapter_id: str, query: str) -> str:
    """Tra thêm SGK theo một câu hỏi (dùng khi bước kiểm tra thấy thiếu kiến thức)."""
    use_rerank = subject not in NO_RERANK
    try:
        docs = retriever.search_sgk(query, subject, chapter_id, k=SGK_FETCH if use_rerank else SGK_PER_LESSON)
        if use_rerank:
            docs = retriever.rerank(query, docs, top_k=SGK_PER_LESSON)
    except Exception as e:
        print(f"[ctx] lỗi tra thêm SGK {subject} chương {chapter_id}: {type(e).__name__} {str(e)[:150]}")
        return ""
    return "\n".join(f"- {d.page_content[:SGK_MAX_CHARS]}" for d in docs)