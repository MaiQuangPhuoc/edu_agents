import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.documents import Document

from src.edu_qa.state import RetrievedChunk
from src.edu_qa.tools.web_search_tool import web_search_edu

# retriever's CrossEncoder trả score 0-1
ROUND1_K, ROUND1_TOPK, ROUND1_SCORE = 15, 3, 0.7
ROUND2_K, ROUND2_TOPK, ROUND2_SCORE = 30, 5, 0.6
WEB_TOPK, WEB_SCORE = 3, 0.5

TOOLS_TOP_K = 3
TOOLS_SCORE_THRESHOLD = 0.3

# filter chunk not duplicate by chunk_id, then sort by score descending, then take top-k
def dedupe_by_chunk_id(docs: list[Document]) -> list[Document]:
    seen = set()
    unique = []
    for doc in docs:
        cid = doc.metadata.get("chunk_id")
        if cid is not None and cid in seen:
            continue
        if cid is not None:
            seen.add(cid)
        unique.append(doc)
    return unique


# Retrieve, rerank, and filter documents based on a score threshold
def retrieve_rerank_filter(retriever, query: str, subject: str, k: int, top_k: int, score_threshold: float) -> list[Document]:
    docs = retriever.hybrid_search_qa(query, k=k, subject=subject)
    reranked = retriever.rerank(query, docs, top_k=top_k)
    filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= score_threshold]
    return dedupe_by_chunk_id(filtered)


def run_cascade_retrieve(retriever, query: str, subject: str) -> list[Document]:
    round1 = retrieve_rerank_filter(retriever, query, subject, ROUND1_K, ROUND1_TOPK, ROUND1_SCORE)
    if round1:
        return round1

    round2 = retrieve_rerank_filter(retriever, query, subject, ROUND2_K, ROUND2_TOPK, ROUND2_SCORE)
    if round2:
        return round2

    return []


def web_fallback(retriever, query: str, subject: str) -> list[Document]:
    web_results = web_search_edu.invoke({"query": query, "subject": subject, "max_results": WEB_TOPK})
    if not web_results:
        return []

    web_docs = [
        Document(
            page_content=r["content"],
            metadata={"source": r.get("url", ""), "chunk_id": None, "is_web": True},
        )
        for r in web_results
    ]
    reranked = retriever.rerank(query, web_docs, top_k=WEB_TOPK)
    return [d for d in reranked if d.metadata.get("rerank_score", 0) >= WEB_SCORE]


def docs_to_chunks(docs: list[Document]) -> list[RetrievedChunk]:
    print("================== qa_retrieval_utils.py ================== ")
    chunks = []
    for d in docs:
        content = d.page_content
        if d.metadata.get("is_web"):
            content = f"[Nguồn: Internet - {d.metadata.get('source', '')}]\n{content}"
        chunks.append(RetrievedChunk(
            content=content,
            source=d.metadata.get("lesson") or d.metadata.get("chapter_name", "unknown"),
            chapter=d.metadata.get("chapter_name"),
            score=d.metadata.get("rerank_score", 0.0),
            chunk_id=d.metadata.get("chunk_id"),
        ))
    return chunks


def retrieve_tools(retriever, query: str, top_k: int = TOOLS_TOP_K) -> list[Document]:
    """Rerank top-k tool phù hợp nhất từ collection tools, dựa trên query (sub_query.text + context)."""
    docs = retriever.hybrid_search_tools(query, k=15)
    reranked = retriever.rerank(query, docs, top_k=top_k)
    return reranked

print(" qa_retrieval_utils.py loaded successfully")