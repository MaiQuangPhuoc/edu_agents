import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from src.state_plan import PlanState, GuardResult
from src.clients.llm import LLMClient
from src.edu_qa.paths import GUARD_PROMPT_PATH
from src.edu_planning.collect_student_model import collect_student_model
from src.edu_planning.planning_agent import make_planning_graph

def _history_text(messages: list) -> str:
    lines = [f"{'Học sinh' if isinstance(m, HumanMessage) else 'Trợ lý'}: {m.content}" for m in messages[-12:]]
    return "\n".join(lines) or "(chưa có)"

def make_roadmap_graph(retriever, llm_client: LLMClient, checkpointer=None):
    planning = make_planning_graph(retriever, llm_client)   # graph con, dùng chung PlanState

    def guard(state: PlanState) -> dict:
        last = next((m.content for m in reversed(state.get("messages", [])) if isinstance(m, HumanMessage)), "")
        if not last:
            return {"guard_ok": True}
        prompt = (GUARD_PROMPT_PATH.read_text(encoding="utf-8")
                  .replace("{message}", last)
                  .replace("{history}", _history_text(state.get("messages", []))))
        res = llm_client.invoke_structured(GuardResult, [{"role": "user", "content": prompt}], max_tokens=300)
        if res is None or res.hop_le:          # lỗi thì cho qua
            return {"guard_ok": True}
        return {"guard_ok": False, "messages": [AIMessage(content=res.tra_loi)]}

    def collect(state: PlanState) -> dict:
        return collect_student_model(state, llm_client)

    def after_guard(state: PlanState) -> str:
        if not state.get("guard_ok", True) or state.get("roadmap_status") == "approved":
            return END
        if state.get("roadmap_status") == "updating_profile" or not state.get("model_done"):
            return "collect"
        return "planning"

    def after_collect(state: PlanState) -> str:
        if state.get("roadmap_status") == "profile_changed":
            return "planning"
        if state.get("roadmap_status") == "updating_profile":
            return END
        return "planning" if state.get("model_done") else END

    def after_planning(state: PlanState) -> str:
        return "collect" if state.get("roadmap_status") == "updating_profile" else END

    g = StateGraph(PlanState)
    g.add_node("guard", guard)
    g.add_node("collect", collect)
    g.add_node("planning", planning)
    g.add_edge(START, "guard")
    g.add_conditional_edges("guard", after_guard, {"collect": "collect", "planning": "planning", END: END})
    g.add_conditional_edges("collect", after_collect, {"planning": "planning", END: END})
    g.add_conditional_edges("planning", after_planning, {"collect": "collect", END: END})
    return g.compile(checkpointer=checkpointer)