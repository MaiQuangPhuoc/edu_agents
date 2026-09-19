import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from functools import partial
from langgraph.graph import StateGraph, END

from src.clients.llm import LLMClient
from src.state_edu import ExamState

from src.edu_exam.collect_info_v2 import collect_info as _collect_info
from src.edu_exam.retrieve_docs_v2 import retrieve_docs as _retrieve_docs
from src.edu_exam.build_knowledge_v2 import build_knowledge as _build_knowledge
from src.edu_exam.build_matrix_v2 import build_matrix as _build_matrix
from src.edu_exam.build_specs_v2 import build_specs as _build_specs
from src.edu_exam.generate_questions_v2 import generate_questions as _generate_questions
from src.edu_exam.evaluate_exam_v2 import evaluate_exam as _evaluate_exam


def create_graph(llm_client: LLMClient, retriever) -> StateGraph:
    """Build LangGraph orchestration cho flow tạo đề thi.
    Lưu ý: graph.py chỉ orchestration, toàn bộ logic nằm trong từng file agent tương ứng.
    """
    g = StateGraph(ExamState)

    g.add_node("collect_info",       partial(_collect_info,       llm_client=llm_client))
    g.add_node("retrieve_docs", partial(_retrieve_docs, llm_client=llm_client, retriever=retriever))   # ← bỏ top_k=5
    g.add_node("build_knowledge",    partial(_build_knowledge,    llm_client=llm_client))
    g.add_node("build_matrix",       partial(_build_matrix,       llm_client=llm_client))
    g.add_node("build_specs",        partial(_build_specs,        llm_client=llm_client))
    g.add_node("generate_questions", partial(_generate_questions, llm_client=llm_client))
    g.add_node("evaluate_exam", partial(_evaluate_exam, llm_client=llm_client, retriever=retriever))

    g.set_entry_point("collect_info")

    g.add_conditional_edges(
        "collect_info",
        lambda state: "retrieve_docs" if state.get("profile_complete") else END,
        {"retrieve_docs": "retrieve_docs", END: END},
    )

    g.add_conditional_edges(
        "retrieve_docs",
        lambda state: "build_knowledge" if state.get("retrieve_complete") else END,
        {"build_knowledge": "build_knowledge", END: END},
    )

    g.add_conditional_edges(
        "build_knowledge",
        lambda state: "build_matrix" if state.get("knowledge_done") else END,
        {"build_matrix": "build_matrix", END: END},
    )

    g.add_conditional_edges(
        "build_matrix",
        lambda state: "build_specs" if state.get("matrix_done") else END,
        {"build_specs": "build_specs", END: END},
    )

    g.add_conditional_edges(
        "build_specs",
        lambda state: "generate_questions" if state.get("specs_done") else END,
        {"generate_questions": "generate_questions", END: END},
    )

    g.add_edge("generate_questions", "evaluate_exam")

    g.add_conditional_edges(
        "evaluate_exam",
        lambda state: "generate_questions" if not state.get("evaluate_done") else END,
        {"generate_questions": "generate_questions", END: END},
    )

    return g.compile()
