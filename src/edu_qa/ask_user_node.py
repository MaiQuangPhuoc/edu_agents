import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import AIMessage
from src.edu_qa.qa_state import QAState
from src.clients.llm import LLMClient

PROMPT_PATH = Path(r'D:\VKU\Nam_4\ky_I\computer_vision\EDUAGENT\prompt_edu\prompt\qa_clarify.txt')


def ask_user_node(state: QAState, llm_client: LLMClient) -> dict:
    print(">>> [Node] ask_user_node")

    question = state.get("question", "")
    template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = template.replace("{question}", question)

    response = llm_client._llm.invoke([{"role": "user", "content": prompt}])
    clarify_question = response.content.strip()

    print(f">>> ask_user_node: clarify_question={clarify_question}")

    return {
        "messages":          [AIMessage(content=clarify_question)],
        "clarify_question":  clarify_question,
        "awaiting_user":     True,
    }