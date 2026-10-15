from langchain_core.messages import AIMessage
import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langgraph.graph import StateGraph, START, END
from src.state_plan import PlanState
from src.clients.llm import LLMClient
from src.edu_planning.lp_plan import plan_node, replan_node, find_gaps
from src.edu_planning.lp_execute import execute_node
from src.edu_planning.lp_assemble import assemble_node
from src.edu_planning.lp_critic import critic_node


def _format_path(lp: dict, issues: dict) -> str:
    sc = lp["schedule"]
    lines = [f"**Kế hoạch học chi tiết (giai đoạn {lp['current_phase']})**",
             f"{sc['sessions_per_week']} buổi/tuần, mỗi buổi {sc['minutes_per_session']} phút, bắt đầu {sc['start_date']}."]
    for wk in lp["weeks"]:
        lines.append(f"\n**Tuần {wk['week_no']}** ({wk['start_date']} → {wk['end_date']}): {wk['goal']}")
        for s in wk["sessions"]:
            lines.append(f"\n- **{s['date']} {s['start_time']}** ({s['minutes']} phút, {s['type']}, độ khó {s['difficulty']}): "
                         f"chương {s['chapter_id']} — {s['lesson']}")
            if s["must_know"]:
                lines.append("  - Cần nắm: " + "; ".join(s["must_know"]))
            if s["must_understand"]:
                lines.append("  - Cần hiểu: " + "; ".join(s["must_understand"]))
            if s["related"]:
                lines.append("  - Liên hệ: " + "; ".join(f"{r['lesson']} ({r['relation']})" for r in s["related"]))
            lines += [f"  - {a['type']} ({a['minutes']} phút, {a['difficulty']}): {a['content']}" for a in s["activities"]]
            lines += [f"  - {r['type']}: {r['title']} ({r.get('url', '')})" for r in s["resources"]]
            if s.get("assessment"):
                a = s["assessment"]
                lines.append(f"  - Bài test: {a['num_questions']} câu, chương {', '.join(a['chapter_ids'])}")
    if issues:
        lines.append("\n*Một số chỗ chưa khớp hoàn toàn quy tắc, mình ghi nhận để chỉnh sau.*")
    lines.append("\nBạn thấy kế hoạch này thế nào?")
    return "\n".join(lines)


def present_node(state: PlanState) -> dict:
    draft = state.get("lp_draft", {})
    if not draft or "error" in draft:
        msg = "Mình chưa soạn được kế hoạch chi tiết" + (f": {draft['error']}" if draft.get("error") else ".")
    else:
        msg = _format_path(draft, state.get("lp_issues", {}))
    return {"messages": [AIMessage(content=msg)], "learning_path": draft, "roadmap_status": "path_ready"}


def route_after_execute(state: PlanState) -> str:
    return "replan" if find_gaps(state) and state.get("lp_replan_count", 0) < 1 else "assemble"


def route_after_critic(state: PlanState) -> str:
    return "assemble" if state.get("lp_issues") and state.get("lp_revision_count", 0) < 2 else "present"


def make_learning_path_graph(retriever, llm_client: LLMClient, checkpointer=None):
    g = StateGraph(PlanState)
    g.add_node("plan", lambda s: plan_node(s, llm_client))
    g.add_node("execute", lambda s: execute_node(s, retriever, llm_client))
    g.add_node("replan", lambda s: replan_node(s, llm_client))
    g.add_node("assemble", lambda s: assemble_node(s, llm_client))
    g.add_node("critic", critic_node)
    g.add_node("present", present_node)

    g.add_edge(START, "plan")
    g.add_edge("plan", "execute")
    g.add_conditional_edges("execute", route_after_execute, {"replan": "replan", "assemble": "assemble"})
    g.add_edge("replan", "execute")
    g.add_edge("assemble", "critic")
    g.add_conditional_edges("critic", route_after_critic, {"assemble": "assemble", "present": "present"})
    g.add_edge("present", END)
    return g.compile(checkpointer=checkpointer)