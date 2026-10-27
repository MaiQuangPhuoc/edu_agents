import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from concurrent.futures import ThreadPoolExecutor
from src.edu_exam.curriculum import get_subject_curriculum

GA_MAX_CHARS = 2500       # tổng ký tự giáo án cho một bài
SGK_FETCH = 8             # số đoạn SGK lấy về cho mỗi bài
SGK_PER_LESSON = 3        # số đoạn SGK giữ lại
SGK_MAX_CHARS = 500
SGK_RERANK_BELOW = 0.0    # rerank khi điểm truy xuất cao nhất < ngưỡng này; 0.0 = chỉ rerank khi thiếu đoạn. Chỉnh theo log "[ctx] sgk".


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
    """{tên bài: văn bản giáo án}; chỉ gồm bài có giáo án."""
    try:
        by_title = retriever.lesson_plan_lessons(subject, chapter_id)
    except Exception as e:
        print(f"[ctx] lỗi giáo án {subject} chương {chapter_id}: {type(e).__name__} {str(e)[:150]}")
        return {}
    out = {}
    for name in lessons:
        title = _match(name, list(by_title))
        if title:
            out[name] = "\n".join(d.page_content for d in by_title[title])[:GA_MAX_CHARS]
    return out


def _sgk_docs(retriever, subject: str, chapter_id: str, query: str) -> tuple[list, str]:
    """Lấy SGK theo query; chỉ rerank khi truy xuất kém (thiếu đoạn hoặc điểm cao nhất dưới ngưỡng)."""
    docs = retriever.search_sgk(query, subject, chapter_id, k=SGK_FETCH)
    scores = [d.metadata.get("retrieve_score") for d in docs]
    top = max((s for s in scores if s is not None), default=None)
    poor = bool(docs) and (len(docs) < SGK_PER_LESSON or (top is not None and top < SGK_RERANK_BELOW))
    if poor:
        docs = retriever.rerank(query, docs, top_k=SGK_PER_LESSON)
    return docs[:SGK_PER_LESSON], f"top={'-' if top is None else f'{top:.3f}'} n={len(scores)} rerank={poor}"


def _sgk_ctx(retriever, subject: str, chapter_id: str, chapter: dict, names: list) -> dict:
    out = {}
    for name in names:
        secs = [s for s in chapter["lessons"][name] if s != name][:4]
        q = f"{chapter['chapter_name']} {name} {'; '.join(secs)}".strip()
        try:
            docs, info = _sgk_docs(retriever, subject, chapter_id, q)
        except Exception as e:
            print(f"[ctx] lỗi SGK {subject} chương {chapter_id} bài {name}: {type(e).__name__} {str(e)[:150]}")
            continue
        print(f"[ctx] sgk {subject} chương {chapter_id} | {name} | {info}")
        if docs:
            out[name] = "\n".join(f"- {d.page_content[:SGK_MAX_CHARS]}" for d in docs)
    return out


def chapter_contexts(retriever, subject: str, chapter_id: str) -> dict:
    """Ngữ cảnh từng bài của một chương: giáo án và SGK lấy song song, bài nào cũng có cả hai nếu tìm được.
    Trả {"lessons": {tên bài: {"plan": str, "sgk": str}}}."""
    chapter = get_subject_curriculum(subject).get(chapter_id)
    if not chapter:
        return {"lessons": {}}
    names = list(chapter["lessons"])
    with ThreadPoolExecutor(max_workers=2) as ex:
        f_plan = ex.submit(_lesson_plan_ctx, retriever, subject, chapter_id, names)
        f_sgk = ex.submit(_sgk_ctx, retriever, subject, chapter_id, chapter, names)
        plan, sgk = f_plan.result(), f_sgk.result()
    return {"lessons": {n: {"plan": plan.get(n, ""), "sgk": sgk.get(n, "")} for n in names}}
