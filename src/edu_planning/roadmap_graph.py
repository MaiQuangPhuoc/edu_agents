import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from src.state_plan import PlanState, GuardResult
from src.clients.llm import LLMClient, build_prompt_messages
from src.edu_qa.paths import GUARD_PROMPT_PATH
from src.edu_planning.collect_student_model import collect_student_model
from src.edu_planning.entry_test import entry_test_node
from src.edu_planning.entry_grade import entry_grade_node
from src.edu_planning.planning_agent import make_planning_graph
from src.edu_planning.learning_path_graph import make_learning_path_graph
from src.configs import env_config

def _history_text(messages: list) -> str:
    lines = [f"{'Học sinh' if isinstance(m, HumanMessage) else 'Trợ lý'}: {m.content}" for m in messages[-12:]]
    return "\n".join(lines) or "(chưa có)"

def make_roadmap_graph(retriever, llm_client: LLMClient, checkpointer=None):
    # planning = make_planning_graph(retriever, llm_client)   # graph con, dùng chung PlanState
    plan_client = LLMClient(model=env_config.plan_model, api_provider=env_config.plan_provider)   # Luna cho sườn
    planning = make_planning_graph(retriever, llm_client, plan_client=plan_client)   # graph con, dùng chung PlanState
    learning_path = make_learning_path_graph(retriever, llm_client)
    guard_client = LLMClient(model=env_config.guard_model, api_provider=env_config.api_provider)

    def guard(state: PlanState) -> dict:
        print(f"model guard: {env_config.guard_model}, provider: {env_config.api_provider}")
        if state.get("roadmap_status") == "awaiting_test_answers":    # tin nhắn là đáp án bài test, không cần lọc
            return {"guard_ok": True}
        last = next((m.content for m in reversed(state.get("messages", [])) if isinstance(m, HumanMessage)), "")
        if not last:
            return {"guard_ok": True}
        messages = build_prompt_messages(GUARD_PROMPT_PATH, {
            "history": _history_text(state.get("messages", [])),
            "message": last,
        })

        res = guard_client.invoke_structured(GuardResult, messages, max_tokens=1000)

        if res is None or res.hop_le:          # lỗi thì cho qua
            return {"guard_ok": True}
        return {"guard_ok": False, "messages": [AIMessage(content=res.tra_loi)]}

    def collect(state: PlanState) -> dict:
        return collect_student_model(state, llm_client)

    def after_guard(state: PlanState) -> str:
        if not state.get("guard_ok", True) or state.get("roadmap_status") in ("approved", "path_ready"):
            return END
        if state.get("roadmap_status") == "path_failed":          # soạn lộ trình lỗi: tin nhắn tiếp theo = thử lại
            return "learning_path"
        if state.get("roadmap_status") == "awaiting_test_answers":
            return "entry_grade"
        if state.get("roadmap_status") == "entry_test_failed":     # tạo đề lỗi: tin nhắn tiếp theo = thử lại
            return "entry_test"
        if state.get("roadmap_status") == "updating_profile" or not state.get("model_done"):
            return "collect"
        return "planning" if state.get("entry_done") else "entry_test"

    def after_collect(state: PlanState) -> str:
        if state.get("roadmap_status") == "profile_changed":
            return "planning"
        if state.get("roadmap_status") == "updating_profile":
            return END
        if not state.get("model_done"):
            return END
        return "planning" if state.get("entry_done") else "entry_test"

    def after_planning(state: PlanState) -> str:
        status = state.get("roadmap_status")
        if status == "updating_profile":
            return "collect"
        return "learning_path" if status == "approved" else END

    g = StateGraph(PlanState)
    g.add_node("guard", guard)
    g.add_node("collect", collect)
    g.add_node("entry_test", entry_test_node)
    g.add_node("entry_grade", lambda s: entry_grade_node(s, llm_client))
    g.add_node("planning", planning)
    g.add_node("learning_path", learning_path)
    g.add_edge(START, "guard")
    g.add_conditional_edges("guard", after_guard, {"collect": "collect", "planning": "planning", "learning_path": "learning_path",
                                                     "entry_test": "entry_test", "entry_grade": "entry_grade", END: END})
    g.add_conditional_edges("collect", after_collect, {"planning": "planning", "entry_test": "entry_test", END: END})
    g.add_edge("entry_test", END)
    g.add_conditional_edges("entry_grade", lambda s: "planning" if s.get("entry_done") else END,
                            {"planning": "planning", END: END})
    g.add_conditional_edges("planning", after_planning,
                            {"collect": "collect", "learning_path": "learning_path", END: END})
    g.add_edge("learning_path", END)
    return g.compile(checkpointer=checkpointer)