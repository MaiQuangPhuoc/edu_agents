import json, re
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import AIMessage
from src.edu_qa.qa_state import QAState
from src.clients.llm import LLMClient

PROMPT_PATH = Path(r'D:\VKU\Nam_4\ky_I\computer_vision\EDUAGENT\prompt_edu\prompt\qa_router.txt')


def _parse_router(text: str) -> dict:
    text = re.sub(r'^```(?:json)?\s*', '', text.strip(), flags=re.IGNORECASE)
    text = re.sub(r'\s*```$', '', text.strip())
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError("Không tìm thấy JSON object")
    return json.loads(match.group())


def router_node(state: QAState, llm_client: LLMClient) -> dict:
    print(">>> [Node] router_node")

    question = state.get("question", "")
    template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = template.replace("{question}", question)

    result = {"loai": "mo_ho", "can_retrieve": False}
    for attempt in range(3):
        response = llm_client._llm.invoke([{"role": "user", "content": prompt}])
        try:
            parsed = _parse_router(response.content)
            result["loai"] = parsed.get("loai", "mo_ho")
            result["can_retrieve"] = bool(parsed.get("can_retrieve", False))
            break
        except Exception as e:
            print(f"[router_node] attempt {attempt} lỗi: {e}")

    print(f">>> router_node: loai={result['loai']} | can_retrieve={result['can_retrieve']}")

    return {
        "loai":         result["loai"],
        "can_retrieve": result["can_retrieve"],
    }