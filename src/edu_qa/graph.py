import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from functools import partial
from langgraph.graph import StateGraph, END

from src.clients.llm import LLMClient
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.edu_qa.state import QAState
from src.edu_qa.qa_router_agent import run_qa_router_agent
from src.edu_qa.qa_rag_agent import run_qa_rag_agent
from src.edu_qa.qa_solve_agent import run_qa_solve_agent
from src.edu_qa.qa_format_agent import run_qa_format_agent


def route_after_router(state: QAState) -> str:
    if state.router_output.loai == 1:
        return "qa_format"
    return "qa_rag"


def route_after_rag(state: QAState) -> str:
    if state.router_output.loai == 3:
        return "qa_solve"
    return "qa_format"


def build_qa_graph(llm_client: LLMClient, retriever: VectorStoreRetriever):
    g = StateGraph(QAState)

    g.add_node("qa_router", partial(run_qa_router_agent, llm_client=llm_client))
    g.add_node("qa_rag",    partial(run_qa_rag_agent, llm_client=llm_client, retriever=retriever))
    g.add_node("qa_solve",  partial(run_qa_solve_agent, llm_client=llm_client, retriever=retriever))
    g.add_node("qa_format", partial(run_qa_format_agent, llm_client=llm_client))

    g.set_entry_point("qa_router")

    g.add_conditional_edges(
        "qa_router", route_after_router,
        {"qa_format": "qa_format", "qa_rag": "qa_rag"},
    )
    g.add_conditional_edges(
        "qa_rag", route_after_rag,
        {"qa_solve": "qa_solve", "qa_format": "qa_format"},
    )
    g.add_edge("qa_solve", "qa_format")
    g.add_edge("qa_format", END)

    return g.compile()

print("QA graph built successfully")