import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document

from src.clients.llm import LLMClient
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.edu_qa.state import QAState, SubQuery, RagResult, RetrievedChunk
from src.edu_qa.tools.web_search_tool import web_search_math
from src.edu_qa.paths import PROMPT_DIR

BATCH_PROMPT_PATH = PROMPT_DIR / "qa_rag_batch_prompt.txt"

INITIAL_K = 3
K_STEP = 3
THRESHOLD_HIGH = 0.8
THRESHOLD_LOW = 0.7
BATCH_SIZE = 3
NO_ANSWER_MARKER = "Không biết"


class SubQueryAnswer(BaseModel):
    sub_query_id: str = Field(..., description="ID của sub-query, khớp đúng với sub_query_id đã đưa vào")
    ket_qua: str = Field(..., description="Câu trả lời dựa trên context đã cho")


class BatchAnswer(BaseModel):
    items: list[SubQueryAnswer] = Field(..., description="Kết quả cho từng sub-query trong batch, đủ số lượng đã đưa vào")


# ── Bước 1: retrieve + rerank + lọc theo ngưỡng (code thuần, không LLM) ────

MAX_CONTEXT_CHUNKS = 3

def _filter_and_cap(docs: list, threshold: float, max_chunks: int = MAX_CONTEXT_CHUNKS) -> list:
    """Lấy toàn bộ chunk vượt ngưỡng, nếu nhiều hơn max_chunks thì giữ top max_chunks điểm cao nhất."""
    filtered = [d for d in docs if d.metadata.get("rerank_score", 0.0) >= threshold]
    if len(filtered) <= max_chunks:
        return filtered
    filtered_sorted = sorted(filtered, key=lambda d: d.metadata.get("rerank_score", 0.0), reverse=True)
    return filtered_sorted[:max_chunks]


def _rerank_from_vectordb(retriever: VectorStoreRetriever, query: str, k: int) -> list:
    candidates = retriever.hybrid_search(query)
    return retriever.rerank(query, candidates, top_k=k)


def _web_results_to_documents(results: list[dict]) -> list[Document]:
    return [
        Document(page_content=r["content"], metadata={"title": r["title"], "url": r["url"]})
        for r in results
    ]


def _get_context_for_query(retriever: VectorStoreRetriever, query: str) -> tuple[list, str]:
    # Vòng 1: lấy nhiều ứng viên để rerank, ngưỡng cao
    reranked = _rerank_from_vectordb(retriever, query, k=10)
    filtered = _filter_and_cap(reranked, THRESHOLD_HIGH)
    if filtered:
        return filtered, "rag"

    # Vòng 2: tăng số ứng viên rerank, hạ ngưỡng
    reranked = _rerank_from_vectordb(retriever, query, k=15)
    filtered = _filter_and_cap(reranked, THRESHOLD_LOW)
    if filtered:
        return filtered, "rag"

    # Fallback: web search, 1 lần duy nhất
    web_results = web_search_math.invoke({"query": query})
    if web_results:
        web_docs = _web_results_to_documents(web_results)
        web_reranked = retriever.rerank(query, web_docs, top_k=10)
        filtered = _filter_and_cap(web_reranked, THRESHOLD_LOW)
        if filtered:
            return filtered, "web_search"

    return [], "none"


def _to_retrieved_chunks(docs: list) -> list[RetrievedChunk]:
    return [
        RetrievedChunk(
            content=d.page_content,
            source=f"{d.metadata.get('chapter_name', '')} - Bài {d.metadata.get('lesson_name', '')}" if d.metadata.get("chapter_name") else d.metadata.get("title", "web"),
            chapter=d.metadata.get("chapter_id"),
            score=d.metadata.get("rerank_score", 0.0),
        )
        for d in docs
    ]


# ── Bước 2: gọi LLM theo batch tối đa BATCH_SIZE cặp/lần ───────────────────

def _build_items_text(pairs: list[tuple[str, str, list]]) -> str:
    parts = []
    for sub_query_id, question_text, docs in pairs:
        context_text = "\n".join(d.page_content for d in docs)
        parts.append(
            f"sub_query_id: {sub_query_id}\n"
            f"query: {question_text}\n"
            f"context:\n{context_text}"
        )
    return "\n\n---\n\n".join(parts)


async def _call_llm_batch(pairs: list[tuple[str, str, list]], llm_client: LLMClient) -> BatchAnswer:
    template = BATCH_PROMPT_PATH.read_text(encoding="utf-8")
    items_text = _build_items_text(pairs)
    prompt_text = template.format(items_text=items_text)
    messages = [HumanMessage(content=prompt_text)]

    result: BatchAnswer = await llm_client.ainvoke_with_retries(
        prompt=messages, output_model=BatchAnswer, temperature=0.0,
    )
    return result


def _chunk_list(items: list, size: int) -> list[list]:
    return [items[i:i + size] for i in range(0, len(items), size)]


# ── Node chính ───────────────────────────────────────────────────────────────

async def run_qa_rag_agent(
    state: QAState,
    llm_client: LLMClient,
    retriever: VectorStoreRetriever,
) -> QAState:
    queries: list[SubQuery] = state.router_output.sub_queries

    rag_results: list[RagResult] = []
    valid_pairs: list[tuple[str, str, list]] = []  # (sub_query_id, text, docs) có context hợp lệ

    # Bước 1: lấy context cho từng sub_query (code thuần, không LLM)
    for q in queries:
        docs, source = _get_context_for_query(retriever, q.text)

        if not docs:
            rag_results.append(RagResult(
                sub_query_id=q.id,
                chunks=[],
                is_sufficient=False,
                answer=NO_ANSWER_MARKER,
                retrieve_round=2,
            ))
        else:
            valid_pairs.append((q.id, q.text, docs))

    # Bước 2: gọi LLM theo batch tối đa BATCH_SIZE cặp/lần
    for batch in _chunk_list(valid_pairs, BATCH_SIZE):
        batch_answer = await _call_llm_batch(batch, llm_client)
        answer_map = {item.sub_query_id: item.ket_qua for item in batch_answer.items}
        docs_map = {sub_query_id: docs for sub_query_id, _, docs in batch}

        for sub_query_id, _, docs in batch:
            rag_results.append(RagResult(
                sub_query_id=sub_query_id,
                chunks=_to_retrieved_chunks(docs),
                is_sufficient=True,
                answer=answer_map.get(sub_query_id, NO_ANSWER_MARKER),
                retrieve_round=1,
            ))

    state.rag_results = rag_results
    return state