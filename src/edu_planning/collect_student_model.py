import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage
from src.clients.llm import LLMClient
from src.edu_qa.paths import COLLECT_STUDENT_MODEL_PROMPT_PATH
from src.edu_planning.student_store import save_student_model
from src.state_plan import PlanState, StudentModel, CollectTurn, AgentMessage


def _history_text(messages: list) -> str:
    lines = [f"{'Học sinh' if isinstance(m, HumanMessage) else 'Trợ lý'}: {m.content}" for m in messages[-12:]]
    return "\n".join(lines) or "(chưa có)"


def collect_student_model(state: PlanState, llm_client: LLMClient) -> dict:
    if state.get("model_done", False):
        return {"current_step": "collect_student_model"}

    student_id = state.get("student_id", "")
    current = state.get("student_model") or StudentModel(student_id=student_id).model_dump(mode="json")

    prompt = (COLLECT_STUDENT_MODEL_PROMPT_PATH.read_text(encoding="utf-8")
              .replace("{thong_tin_da_co}", json.dumps(current, ensure_ascii=False, indent=2))
              .replace("{history}", _history_text(state.get("messages", []))))

    turn = llm_client.invoke_structured(CollectTurn, [{"role": "user", "content": prompt}], max_tokens=3000)
    if turn is None:
        return {"messages": [AIMessage(content="Bạn nhắc lại giúp mình nhé?")], "current_step": "collect_student_model"}

    model = turn.student_model.model_dump(mode="json")
    model["student_id"] = student_id
    model["tien_do"] = current.get("tien_do", {})      # phần của Progress Agent, không để LLM ghi đè
    model["updated_at"] = datetime.now().isoformat()

    if turn.hoan_tat:
        save_student_model(model)


    inbox = list(state.get("a2a_inbox", []))
    if turn.hoan_tat:
        inbox.append(AgentMessage(
            sender="student_model", receiver="planning",
            type="result", payload={"student_model": model},
        ).model_dump(mode="json"))

    return {
        "messages":      [AIMessage(content=turn.tin_nhan)],
        "student_model": model,
        "model_done":    turn.hoan_tat,
        "a2a_inbox":     inbox,
        "current_step":  "collect_student_model",
    }