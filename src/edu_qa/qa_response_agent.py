import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import datetime
from langchain_core.messages import HumanMessage

from src.clients.llm import LLMClient
from src.edu_qa.state import QAState, FormattedAnswer
from src.edu_qa.paths import QA_RESPONSE_PROMPT_PATH, CHAT_LOG_PATH
from src.edu_qa.qa_memory import append_chat_turn


def _build_raw_answers_block(state: QAState) -> str:
    router_output = state.router_output
    sub_query_map = {sq.id: sq.text for sq in router_output.sub_queries}

    if router_output.query_type == "bai_tap":
        blocks = []
        for r in state.solve_results:
            header = f"Sub {r.sub_query_id} - Câu hỏi: {sub_query_map.get(r.sub_query_id, '')}"
            header += f" [tool_used={r.tool_used} | verify_method={r.verify_method} | context_source={r.context_source}]"
            answer_line = f"Kết quả: {r.result}"
            blocks.append("\n".join([header, answer_line]))
        return "\n\n".join(blocks)

    blocks = []
    for r in state.rag_results:
        header = f"Sub {r.sub_query_id} - Câu hỏi: {sub_query_map.get(r.sub_query_id, '')}"
        if r.used_web:
            header += " [used_web=True]"
        answer_line = f"Trả lời: {r.answer}"
        chunk_lines = ["Tài liệu gốc:"]
        if not r.chunks:
            chunk_lines.append("  (không có)")
        else:
            for c in r.chunks:
                chunk_lines.append(f"  [chunk_id: {c.chunk_id} | score: {round(c.score, 3)}] {c.content}")
        blocks.append("\n".join([header, answer_line] + chunk_lines))
    return "\n\n".join(blocks)


def _load_prompt(state: QAState, raw_answers_block: str) -> str:
    template = QA_RESPONSE_PROMPT_PATH.read_text(encoding="utf-8")
    return template.format(
        subject=state.router_output.subject,
        user_query=state.user_query,
        raw_answers_block=raw_answers_block,
    )

# bug add nguoi_dung when user ask question, and add he_thong when system answer
def _format_time_diff(user_time: datetime, system_time: datetime) -> str:
    diff_seconds = int((system_time - user_time).total_seconds())
    if diff_seconds < 60:
        return f"{diff_seconds}s"
    diff_minutes = diff_seconds // 60
    remaining_seconds = diff_seconds % 60
    if remaining_seconds == 0:
        return f"{diff_minutes}p"
    return f"{diff_minutes}p{remaining_seconds}s"


def _append_log_md(state: QAState) -> None:
    CHAT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    user_time_str = state.query_timestamp.strftime("%H:%M:%S %d/%m/%Y") if state.query_timestamp else "?"
    system_time_str = now.strftime("%H:%M:%S %d/%m/%Y")

    time_diff_str = (
        _format_time_diff(state.query_timestamp, now)
        if state.query_timestamp else "?"
    )

    entry = (
        f"Người dùng: {state.user_query} ({user_time_str})\n\n"
        f"Hệ thống: {state.final_answer} ({system_time_str}) - Chênh lệch: {time_diff_str}\n\n"
        f"---\n\n"
    )

    with open(CHAT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)


async def run_qa_response_agent(state: QAState, llm_client: LLMClient) -> QAState:
    raw_answers_block = _build_raw_answers_block(state)
    prompt_text = _load_prompt(state, raw_answers_block)
    messages = [HumanMessage(content=prompt_text)]

    output: FormattedAnswer = await llm_client.ainvoke_with_retries(
        prompt=messages,
        output_model=FormattedAnswer,
        temperature=0.3,
    )

    state.final_answer = output.final_answer
    state.suggestions = output.suggestions

    state = append_chat_turn(state)
    _append_log_md(state)

    print("============================ QA Response Agent Output ============================")
    print(f"Final answer: {state.final_answer}\nSuggestions: {state.suggestions}")
    print("============================ QA Response Agent Output ============================\n\n")

    return state

print("✅ qa_response_agent.py loaded successfully ✅")