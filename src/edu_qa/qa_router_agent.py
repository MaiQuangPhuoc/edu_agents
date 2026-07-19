import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.messages import HumanMessage

from src.clients.llm import LLMClient
from src.edu_qa.state import QAState, RouterOutput
from src.edu_qa.paths import PROMPT_DIR

PROMPT_PATH = PROMPT_DIR / "qa_router_prompt.txt"
MAX_HISTORY_TURNS = 5


def _build_history_text(state: QAState) -> str:
    recent = state.chat_history[-MAX_HISTORY_TURNS:]
    if not recent:
        return "Không có lịch sử, đây là câu hỏi đầu tiên."

    parts = []
    for i, turn in enumerate(recent, start=1):
        parts.append(f"Lượt {i}:\nHọc sinh hỏi: {turn.user_query}\nHệ thống trả lời: {turn.final_answer}")
    return "\n\n".join(parts)


def _load_prompt(state: QAState) -> str:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    history_text = _build_history_text(state)
    return template.format(chat_history_text=history_text, user_query=state.user_query)


async def run_qa_router_agent(state: QAState, llm_client: LLMClient) -> QAState:
    prompt_text = _load_prompt(state)
    messages = [HumanMessage(content=prompt_text)]

    router_output: RouterOutput = await llm_client.ainvoke_with_retries(
        prompt=messages,
        output_model=RouterOutput,
        temperature=0.2,
    )

    state.router_output = router_output
    print("============================ QA Router Agent Output ============================")
    print(f"Router output: loai={router_output.loai}\nly_do={router_output.ly_do}\nsub_queries={router_output.sub_queries}\nclarify_question={router_output.clarify_question}")
    print("============================ QA Router Agent Output ============================\n\n")
    
    return state

print("qa_router_agent.py loaded successfully")