from langchain_core.messages import AIMessage
import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langgraph.graph import StateGraph, START, END
from src.state_plan import PlanState, LearningPath
from src.clients.llm import LLMClient
from src.edu_planning.lp_plan import plan_node
from src.edu_planning.lp_execute import execute_node
from src.edu_planning.lp_assemble import assemble_node
from src.edu_planning.lp_critic import critic_node
from src.edu_planning.lp_outline import outline_node
from src.edu_planning.path_store import save_learning_path
from src.edu_planning.lp_debug import traced


def present_node(state: PlanState) -> dict:
    draft = dict(state.get("lp_draft") or {})
    try:
        if not draft or "error" in draft:
            raise ValueError(draft.get("error", ""))
        draft["assumptions"] = list(draft.get("assumptions", [])) + [
            f"Chưa khớp (tuần {n}): {x}" for n, found in (state.get("lp_issues") or {}).items() for x in found]
        
        first = next((s for w in draft.get("weeks", []) for s in w.get("sessions", [])), None)
        if first:
            first["exam_enabled"] = True                    # mặc định chỉ buổi đầu tiên bật tạo bài ôn tập, các buổi còn lại false

        lp = LearningPath.model_validate(draft).model_dump(mode="json")      # đảm bảo đúng schema trước khi lưu
        sid = state.get("student_id") or state["student_model"].get("student_id", "unknown")
        lp["subject"] = (state.get("lp_window") or {}).get("subject", "")
        roadmap = state.get("master_roadmap") or {}
        lp["overview"] = {k: roadmap.get(k) for k in ("muc_tieu_tong", "chien_luoc", "giai_doan", "gia_dinh")}
        lp["student_model_snapshot"] = state.get("student_model") or {}
        path = save_learning_path(sid, lp)
        lp = json.loads(path.read_text(encoding="utf-8"))
        lp.pop("student_model_snapshot", None)
    except Exception as e:
        msg = "Mình chưa soạn được lộ trình chi tiết" + (f": {str(e)[:200]}" if str(e) else ".") + " Bạn nhắn \"thử lại\" để mình làm lại nhé."
        return {"messages": [AIMessage(content=msg)], "roadmap_status": "path_failed"}
    msg = AIMessage(content="Mình đã soạn xong lộ trình học chi tiết. Bạn bấm nút bên dưới để xem nhé.",
                    additional_kwargs={"action": {"type": "open_learning_path", "student_id": sid, "file": str(path)}})
    return {"messages": [msg], "learning_path": lp, "lp_file": str(path), "roadmap_status": "path_ready"}

def _next_or_present(nxt: str):
    return lambda s: "present" if (s.get("lp_draft") or {}).get("error") else nxt
 
def route_after_critic(state: PlanState) -> str:
    return "assemble" if state.get("lp_issues") and state.get("lp_revision_count", 0) < 3 else "present"


def make_learning_path_graph(retriever, llm_client: LLMClient, plan_client: LLMClient | None = None, checkpointer=None):
    plan_client = plan_client or llm_client          # Luna cho các bước dài; không truyền thì dùng chung 120b
    g = StateGraph(PlanState)
    g.add_node("outline", traced("outline", lambda s: outline_node(s, retriever, plan_client)))
    g.add_node("plan", traced("plan", plan_node))
    g.add_node("execute", traced("execute", lambda s: execute_node(s, retriever, llm_client, plan_client)))
    g.add_node("assemble", traced("assemble", lambda s: assemble_node(s, plan_client)))
    g.add_node("critic", traced("critic", lambda s: critic_node(s, llm_client)))
    g.add_node("present", traced("present", present_node))

    g.add_edge(START, "outline")
    g.add_conditional_edges("outline", _next_or_present("plan"), {"plan": "plan", "present": "present"})
    g.add_conditional_edges("plan", _next_or_present("execute"), {"execute": "execute", "present": "present"})
    g.add_edge("execute", "assemble")
    g.add_edge("assemble", "critic")
    g.add_conditional_edges("critic", route_after_critic, {"assemble": "assemble", "present": "present"})
    g.add_edge("present", END)
    return g.compile(checkpointer=checkpointer)