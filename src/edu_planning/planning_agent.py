import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from src.state_plan import PlanState, MasterRoadmap, AgentMessage
from src.clients.llm import LLMClient

from langgraph.prebuilt import create_react_agent
from langgraph.errors import GraphRecursionError

from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_qa.paths import PLANNING_PROMPT_PATH
from src.edu_planning.planning_tools import make_planning_tools

MAX_STEPS = 6

FINALIZE_RULE = """

QUÁ TRÌNH TRA CỨU CỦA BẠN
{transcript}

YÊU CẦU
Dựa trên hồ sơ, cấu trúc chương trình và quá trình tra cứu ở trên, xuất MasterRoadmap.
chapter_id và tên bài phải lấy đúng từ cấu trúc chương trình. Điểm nào là suy luận thì ghi vào gia_dinh."""


def _curriculum_text(sm: dict) -> str:
    items = (sm.get("nang_luc") or []) + (sm.get("muc_tieu") or [])
    lines = []
    for subject in sorted({x["mon_hoc"] for x in items if x.get("mon_hoc")}):
        for ch_id, ch in get_subject_curriculum(subject).items():
            lines.append(f"[{subject}] chapter_id={ch_id}: {ch['chapter_name']}")
            lines += [f"    - {lesson}" for lesson in ch["lessons"]]
    return "\n".join(lines)


def _build_prompt(state: PlanState) -> str:
    sm = state.get("student_model", {})
    return (PLANNING_PROMPT_PATH.read_text(encoding="utf-8")
            .replace("{student_model}", json.dumps(sm, ensure_ascii=False, indent=2))
            .replace("{curriculum}", _curriculum_text(sm)))


def _transcript(msgs: list) -> str:
    lines = []
    for m in msgs[1:]:
        if isinstance(m, AIMessage):
            calls = ", ".join(f"{c['name']}({c['args']})" for c in (m.tool_calls or []))
            lines.append(f"[Planner] {m.content} {('-> gọi: ' + calls) if calls else ''}".strip())
        elif isinstance(m, ToolMessage):
            lines.append(f"[Kết quả tool] {str(m.content)[:1500]}")
    return "\n".join(lines) or "(không gọi tool)"


def make_planning_graph(retriever, llm_client: LLMClient):
    tools = make_planning_tools(retriever)
    react = create_react_agent(llm_client._llm, tools)

    def planner(state: PlanState) -> dict:
        prompt = _build_prompt(state)
        try:
            res = react.invoke(
                {"messages": [HumanMessage(content=prompt)]},
                config={"recursion_limit": 2 * MAX_STEPS + 1},   # mỗi vòng = 1 lần LLM + 1 lần tool
            )
            msgs = res["messages"]
        except GraphRecursionError:
            print("[planning] vượt giới hạn vòng, chuyển sang finalize không có kết quả tra cứu")
            msgs = [HumanMessage(content=prompt)]
        return {"plan_messages": msgs}

    def finalize(state: PlanState) -> dict:
        msgs = state["plan_messages"]
        prompt = msgs[0].content + FINALIZE_RULE.replace("{transcript}", _transcript(msgs))
        result = llm_client.invoke_structured(MasterRoadmap, [{"role": "user", "content": prompt}], max_tokens=4000)
        if result is None:
            return {"master_done": False, "current_step": "planning"}

        roadmap = result.model_dump()
        inbox = list(state.get("a2a_inbox", []))
        inbox.append(AgentMessage(sender="planning", receiver="roadmap", type="result",
                                  payload={"master_roadmap": roadmap}).model_dump(mode="json"))
        return {"master_roadmap": roadmap, "master_done": True, "a2a_inbox": inbox, "current_step": "planning"}

    g = StateGraph(PlanState)
    g.add_node("planner", planner)
    g.add_node("tools", ToolNode(tools, messages_key="plan_messages"))
    g.add_node("finalize", finalize)
    g.add_edge(START, "planner")
    g.add_conditional_edges("planner", route, {"tools": "tools", "finalize": "finalize"})
    g.add_edge("tools", "planner")
    g.add_edge("finalize", END)
    return g.compile()