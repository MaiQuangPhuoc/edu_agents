import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from functools import partial
from langgraph.graph import StateGraph, END

from src.clients.llm import LLMClient
from src.edu_qa.state import QAState
from src.edu_qa.qa_router_agent import run_qa_router_agent
from src.edu_qa.qa_knowledge_agent import run_qa_knowledge_agent
from src.edu_qa.qa_solve_agent import run_qa_solve_agent
from src.edu_qa.qa_response_agent import run_qa_response_agent
from src.edu_qa.qa_memory import append_chat_turn


async def run_clarify_node(state: QAState) -> QAState:
    """valid=0 -> trả clarify_question, không qua Knowledge/Solve/Response."""
    state.final_answer = state.router_output.clarify_question
    state = append_chat_turn(state)
    return state


def route_after_router(state: QAState) -> str:
    if state.router_output.valid == 0:
        return "clarify"
    if state.router_output.query_type == "bai_tap":
        return "solve"
    return "knowledge"


def build_graph(retriever, llm_client: LLMClient):
    graph = StateGraph(QAState)

    graph.add_node("router", partial(run_qa_router_agent, llm_client=llm_client))
    graph.add_node("knowledge", partial(run_qa_knowledge_agent, retriever=retriever, llm_client=llm_client))
    graph.add_node("solve", partial(run_qa_solve_agent, retriever=retriever, llm_client=llm_client))
    graph.add_node("response", partial(run_qa_response_agent, llm_client=llm_client))
    graph.add_node("clarify", run_clarify_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        route_after_router,
        {
            "clarify": "clarify",
            "solve": "solve",
            "knowledge": "knowledge",
        },
    )

    graph.add_edge("knowledge", "response")
    graph.add_edge("solve", "response")
    graph.add_edge("response", END)
    graph.add_edge("clarify", END)

    return graph.compile()


print("✅ QA graph built successfully ✅")