import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state_edu import ExamState
from src.clients.llm import LLMClient
from src.edu_exam.curriculum import map_scope

ROUND1_K, ROUND1_TOPK, ROUND1_SCORE = 10, 3, 0.6
ROUND2_K, ROUND2_TOPK, ROUND2_SCORE = 15, 5, 0.6


def _retrieve_round(retriever, query: str, ch_id: str, subject: str, seen_ids: set, k: int, top_k: int, score_threshold: float):
    """1 round: fetch (k) → lọc chapter_id → dedup chunk_id → rerank (top_k) → lọc theo score_threshold."""
    docs = retriever.hybrid_search_qa(query, k=k, subject=subject)          # ← hybrid_search_qa, không phải hybrid_search (mới có tham số k)

    docs = [d for d in docs if d.metadata.get("chapter_id") == ch_id]
    docs = [d for d in docs if d.metadata.get("chunk_id") not in seen_ids]

    if not docs:
        return []

    ranked = retriever.rerank(query, docs, top_k=top_k)
    passed = [d for d in ranked if d.metadata.get("rerank_score", 0) >= score_threshold]   # ← lọc score, rerank() không tự làm việc này
    return passed


def _cascade_retrieve_chapter(retriever, query: str, ch_id: str, subject: str, seen_ids: set) -> list:
    """Round 1 hẹp trước (nhanh, ít token) — không đủ mới mở rộng Round 2."""
    result = _retrieve_round(retriever, query, ch_id, subject, seen_ids,
                              k=ROUND1_K, top_k=ROUND1_TOPK, score_threshold=ROUND1_SCORE)

    if len(result) < ROUND1_TOPK:
        print(f"[{ch_id}] Round 1 chỉ {len(result)}/{ROUND1_TOPK} — mở Round 2")
        result = _retrieve_round(retriever, query, ch_id, subject, seen_ids,
                                  k=ROUND2_K, top_k=ROUND2_TOPK, score_threshold=ROUND2_SCORE)

    return result


def retrieve_docs(state: ExamState, llm_client: LLMClient, retriever) -> dict:
    print(">>> [Node] retrieve_docs")

    if state.get("retrieve_complete", False):
        return {"current_step": "retrieve_docs"}

    profile = state.get("student_profile", {})
    subject = profile.get("mon_hoc", "")

    scope_data = map_scope(profile)
    scope_chapters = scope_data["scope_chapters"]
    scope_lessons  = scope_data["scope_lessons"]

    if not scope_chapters:
        print(">>> retrieve_docs: không map được phạm vi kiểm tra")
        return {"retrieved_chunks": [], "current_step": "retrieve_docs"}

    seen_ids = set()
    all_docs = []

    for ch_id, ch_name in scope_chapters.items():
        lessons = scope_lessons.get(ch_id, [])
        lesson_text = ", ".join(lessons)
        query = f"kiến thức nội dung {ch_name}" + (f": {lesson_text}" if lesson_text else "")

        docs = _cascade_retrieve_chapter(retriever, query, ch_id, subject, seen_ids)

        for d in docs:
            seen_ids.add(d.metadata.get("chunk_id"))
        all_docs.extend(docs)

    chunks = [{"content": d.page_content, "metadata": d.metadata} for d in all_docs]

    print(f">>> retrieve_docs: {len(chunks)} chunks sau 2 round")

    return {
        "retrieved_chunks":  chunks,
        "scope_chapters":    scope_chapters,
        "scope_lessons":     scope_lessons,
        "current_step":      "retrieve_docs",
        "retrieve_complete": len(chunks) > 0,
    }