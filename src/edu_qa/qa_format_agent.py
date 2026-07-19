import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.messages import HumanMessage

from src.clients.llm import LLMClient
from src.edu_qa.state import QAState
from src.edu_qa.paths import PROMPT_DIR

PROMPT_PATH = PROMPT_DIR / "qa_format_agent_prompt.txt"


def _build_content_for_loai1(state: QAState) -> str:
    return f"Câu hỏi cần làm rõ: {state.router_output.clarify_question}"


def _build_content_for_loai2(state: QAState) -> str:
    parts = []
    for q in state.router_output.sub_queries:
        rag = next((r for r in state.rag_results if r.sub_query_id == q.id), None)
        answer = rag.answer if rag and rag.answer else "Không tìm được thông tin phù hợp."
        parts.append(f"--- Câu hỏi {q.id}: {q.text} ---\nTrả lời: {answer}")
    return "\n\n".join(parts)


def _build_content_for_loai3(state: QAState) -> str:
    parts = []
    for q in state.router_output.sub_queries:
        solve = next((s for s in state.solve_results if s.sub_query_id == q.id), None)

        if not solve or solve.result == "chưa đủ dữ kiện":
            parts.append(f"--- Câu hỏi {q.id}: {q.text} ---\nKhông đủ dữ kiện để tính toán.")
            continue

        parts.append(
            f"--- Câu hỏi {q.id}: {q.text} ---\n"
            f"Kết quả: {solve.result}\n"
            f"Các bước tính toán: {solve.steps}"
        )
    return "\n\n".join(parts)


def _build_content(state: QAState) -> str:
    loai = state.router_output.loai
    if loai == 1:
        return _build_content_for_loai1(state)
    if loai == 2:
        return _build_content_for_loai2(state)
    return _build_content_for_loai3(state)


async def run_qa_format_agent(state: QAState, llm_client: LLMClient) -> QAState:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    noi_dung = _build_content(state)

    prompt_text = template.format(
        loai=state.router_output.loai,
        ly_do=state.router_output.ly_do,
        noi_dung_theo_loai=noi_dung,
    )
    messages = [HumanMessage(content=prompt_text)]

    response = await llm_client.ainvoke_with_retries(
        prompt=messages,
        temperature=0.3,
    )

    state.final_answer = response.content
    print("============================ QA Format Agent Output ============================")
    print(f"format : {response.content}")
    print("============================ QA Format Agent Output ============================\n\n")

    return state

print("qa_format_agent.py loaded successfully")