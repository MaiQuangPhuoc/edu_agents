import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.messages import HumanMessage

from src.clients.llm import LLMClient
from src.edu_qa.paths import (
    KNOWLEDGE_TOAN_PROMPT_PATH,
    KNOWLEDGE_VAN_PROMPT_PATH,
    KNOWLEDGE_SU_PROMPT_PATH,
) 
from src.edu_qa.qa_memory import build_history_text
from src.edu_qa.qa_retrieval_utils import run_cascade_retrieve, web_fallback, docs_to_chunks
from src.edu_qa.state import QAState, RagResult, RetrievedChunk, KnowledgeAnswerOutput


SUBJECT_PROMPT_MAP = {
    "Toán 10":    KNOWLEDGE_TOAN_PROMPT_PATH,
    "Ngữ văn 10": KNOWLEDGE_VAN_PROMPT_PATH,
    "Lịch sử 10": KNOWLEDGE_SU_PROMPT_PATH,
}


def _build_sub_queries_block(sub_queries) -> str:
    return "\n".join(f"Sub {sq.id}: {sq.text}" for sq in sub_queries)


def _build_context_block(sub_query_id: str, chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return f"(Không có tài liệu liên quan cho Sub {sub_query_id})"
    lines = [f"--- Tài liệu cho Sub {sub_query_id} ---"]
    for c in chunks:
        if c.content.startswith("[Nguồn: Internet"):
            lines.append(c.content)
        else:
            lines.append(f"[Nguồn: {c.source} | Chương/Bài: {c.chapter}]\n{c.content}")
    return "\n\n".join(lines)

async def run_qa_knowledge_agent(state: QAState, retriever, llm_client: LLMClient) -> QAState:
    # get router output from state
    print("================== qa_knowledge_agent.py ================== ")

    router_output = state.router_output
    assert router_output.query_type == "ly_thuyet", (
        f"qa_knowledge_agent chỉ xử lý query_type='ly_thuyet', nhận được '{router_output.query_type}'"
    )
    # get subject and mapping prompt path
    subject = router_output.subject
    prompt_path = SUBJECT_PROMPT_MAP[subject]

    all_chunks_map: dict[str, list[RetrievedChunk]] = {}
    used_web_map: dict[str, bool] = {}

    for sq in router_output.sub_queries:
        docs = run_cascade_retrieve(retriever, sq.retrieval_query, subject)
        used_web = False
        if not docs:
            docs = web_fallback(retriever, sq.retrieval_query, subject)
            used_web = bool(docs)
        all_chunks_map[sq.id] = docs_to_chunks(docs)
        used_web_map[sq.id] = used_web

    sub_queries_block = _build_sub_queries_block(router_output.sub_queries)
    context_block = "\n\n".join(
        _build_context_block(sq.id, all_chunks_map[sq.id]) for sq in router_output.sub_queries
    )
    chat_history_text = build_history_text(state)

    template = prompt_path.read_text(encoding="utf-8")
    prompt_text = template.format(
        chat_history_text=chat_history_text,
        sub_queries_block=sub_queries_block,
        context_block=context_block,
    )

    messages = [HumanMessage(content=prompt_text)]    
    print("="*40)
    print("prompt\n" , messages)
    print("="*40)



    output: KnowledgeAnswerOutput = await llm_client.ainvoke_with_retries(
        prompt=messages,
        output_model=KnowledgeAnswerOutput,
        temperature=0.2,
        num_retries=3,
    )
    print(f"DEBUG - raw output.answers: {output.answers}")
    parsed_answers = {a.sub_query_id: a.answer for a in output.answers}

    rag_results = []
    for sq in router_output.sub_queries:
        chunks = all_chunks_map[sq.id]
        answer = parsed_answers.get(sq.id, "")
        rag_results.append(RagResult(
            sub_query_id=sq.id,
            chunks=chunks,
            is_sufficient=bool(chunks),
            answer=answer,
            retrieve_round=1,
            used_web=used_web_map[sq.id],
        ))

    state.rag_results = rag_results
    print("============================ QA Knowledge Agent Output ============================")
    for r in rag_results:
        print(f"Sub {r.sub_query_id}: is_sufficient={r.is_sufficient}, num_chunks={len(r.chunks)}\nAnswer: {r.answer}")
    print("============================ QA Knowledge Agent Output ============================\n\n")

    return state


async def answer_subquery_as_theory(
    sub_query, subject: str, chat_history_text: str, retriever, llm_client: LLMClient
) -> tuple[str, list, bool]:
    """Trả lời 1 sub_query theo đúng luồng lý thuyết (dùng lại khi Solve Agent không tìm
    được tool phù hợp). Trả về (answer, chunks, used_web)."""
    docs = run_cascade_retrieve(retriever, sub_query.retrieval_query, subject)
    used_web = False
    if not docs:
        docs = web_fallback(retriever, sub_query.retrieval_query, subject)
        used_web = bool(docs)
    chunks = docs_to_chunks(docs)

    sub_queries_block = _build_sub_queries_block([sub_query])
    context_block = _build_context_block(sub_query.id, chunks)

    prompt_path = SUBJECT_PROMPT_MAP[subject]
    template = prompt_path.read_text(encoding="utf-8")
    prompt_text = template.format(
        chat_history_text=chat_history_text,
        sub_queries_block=sub_queries_block,
        context_block=context_block,
    )

    messages = [HumanMessage(content=prompt_text)]
    output: KnowledgeAnswerOutput = await llm_client.ainvoke_with_retries(
        prompt=messages,
        output_model=KnowledgeAnswerOutput,
        temperature=0.2,
    )
    answer = next((a.answer for a in output.answers if a.sub_query_id == sub_query.id), "")
    return answer, chunks, used_web

print("✅ qa_knowledge_agent.py loaded successfully ✅")