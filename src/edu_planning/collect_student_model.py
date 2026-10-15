import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage
from src.clients.llm import LLMClient

from src.edu_planning.student_store import save_student_model
from src.state_plan import PlanState, StudentModel, CollectTurn, CollectPatchTurn, QueryPlan
from src.edu_qa.paths import (COLLECT_STUDENT_MODEL_PROMPT_PATH, COLLECT_UPDATE_PROMPT_PATH,
                              QUERY_TRANSFORM_PROMPT_PATH)

def _history_text(messages: list) -> str:
    lines = [f"{'Học sinh' if isinstance(m, HumanMessage) else 'Trợ lý'}: {m.content}" for m in messages[-12:]]
    return "\n".join(lines) or "(chưa có)"

def _make_queries(model: dict, state: PlanState, llm_client: LLMClient) -> list[dict]:
    shown = {k: v for k, v in model.items() if k != "tien_do"}
    prompt = (QUERY_TRANSFORM_PROMPT_PATH.read_text(encoding="utf-8")
              .replace("{student_model}", json.dumps(shown, ensure_ascii=False, indent=2))
              .replace("{history}", _history_text(state.get("messages", []))))
    res = llm_client.invoke_structured(QueryPlan, [{"role": "user", "content": prompt}], max_tokens=1500)
    return [q.model_dump() for q in res.queries] if res else []


def _update_mode(state: PlanState, llm_client: LLMClient) -> dict:
    req = state["update_request"]
    fields = req.get("fields", [])
    current = state.get("student_model", {})
    shown = {k: v for k, v in current.items() if k != "tien_do"}

    prompt = (COLLECT_UPDATE_PROMPT_PATH.read_text(encoding="utf-8")
              .replace("{fields}", ", ".join(fields))
              .replace("{ly_do}", req.get("ly_do", ""))
              .replace("{student_model}", json.dumps(shown, ensure_ascii=False, indent=2))
              .replace("{history}", _history_text(state.get("messages", []))))

    turn = llm_client.invoke_structured(CollectPatchTurn, [{"role": "user", "content": prompt}], max_tokens=3000)
    if turn is None:
        return {"messages": [AIMessage(content="Bạn nhắc lại phần muốn đổi giúp mình nhé?")],
                "current_step": "collect_student_model"}

    out = {"messages": [AIMessage(content=turn.tin_nhan)], "current_step": "collect_student_model"}
    if not turn.hoan_tat:
        return out

    patch = turn.patch.model_dump(mode="json")
    applied = [f for f in fields if patch.get(f) is not None]     # chỉ nhận nhóm được yêu cầu đổi
    if not applied:
        return out

    new = dict(current)
    for f in applied:
        new[f] = patch[f]
    new["updated_at"] = datetime.now().isoformat()
    save_student_model(new)

    out.update({
        "student_model_prev": current,
        "student_model":      new,
        "roadmap_prev":       state.get("master_roadmap", {}),
        "search_queries":     _make_queries(new, state, llm_client),
        "update_request":     {},
        "roadmap_status":     "profile_changed",
    })
    return out

def collect_student_model(state: PlanState, llm_client: LLMClient) -> dict:
    if state.get("roadmap_status") == "updating_profile" and state.get("update_request"):
        return _update_mode(state, llm_client)

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
    
    queries = _make_queries(model, state, llm_client) if turn.hoan_tat else state.get("search_queries", [])
    
    return {
        "messages":      [AIMessage(content=turn.tin_nhan)],
        "student_model": model,
        "search_queries": queries,
        "model_done":    turn.hoan_tat,
        "current_step":  "collect_student_model",
    }