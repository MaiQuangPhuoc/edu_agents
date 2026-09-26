import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from src.clients.llm import LLMClient
from src.clients.embedding import embeddings_qa
from src.configs import env_config
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever

from src.edu_exam.graph_exam_v2 import create_graph

load_dotenv()


def build_initial_state() -> dict:
    return {
        "messages": [],

        # collect_info
        "student_profile": {},
        "profile_complete": False,

        # retrieve_docs
        "detected_chapters": [],
        "retrieved_chunks": [],
        "retrieve_complete": False,
        "scope_chapters": {},
        "scope_lessons": {},

        # build_knowledge
        "section_selected": False,
        "scored_chunks": [],
        "_pending_sections": [],
        "knowledge_profile": {},
        "knowledge_queue": None,
        "knowledge_pending": None,
        "knowledge_scores": {},
        "knowledge_retried": False,     # ← thêm mới: đánh dấu đã hỏi bù section thiếu điểm chưa
        "knowledge_done": False,
        "completed_build_knowlege": False,

        # build_matrix
        "exam_matrix": {},
        "matrix_done": False,

        # build_specs
        "question_specs": [],
        "specs_done": False,

        # generate_questions
        "generated_exam": [],
        "exam_memory": [],
        "generate_done": False,
        "exam_id": "",

        # evaluate_exam
        "exam_review": {},
        "final_exam": [],
        "evaluate_done": False,
        "regenerate_ids": [],           # ← thêm
        "evaluate_retry_count": 0,  
        "current_step": "",
        "error": None,
    }


def run():
    print("=" * 50)
    print("🎓 Hệ thống tạo đề kiểm tra thông minh")
    print("=" * 50)
    print("Gõ 'q' để thoát\n")

    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)

    # Collection chung cho cả 3 môn (Toán/Văn/Sử), lọc theo metadata["subject"] ở tầng retriever
    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",
        tools_collection_name="tools",     # ← thêm dòng này
        top_k=10,
    )

    graph = create_graph(llm_client, retriever)
    state = build_initial_state()

    while True:
        user_input = input("Học sinh: ").strip()
        if user_input.lower() == "q":
            break
        if not user_input:
            continue

        user_input = "\n".join(line.lstrip("#").strip() for line in user_input.splitlines())
        state["messages"].append(HumanMessage(content=user_input))

        if not state.get("profile_complete"):
            state = graph.invoke(state)
        elif not state.get("knowledge_done"):
            state = graph.invoke(state)
        elif not state.get("matrix_done"):
            state = graph.invoke(state)
        elif not state.get("specs_done"):
            state = graph.invoke(state)
        elif not state.get("generate_done"):
            state = graph.invoke(state)
        elif not state.get("evaluate_done"):
            state = graph.invoke(state)
        else:
            break

        ai_messages = [m for m in state["messages"] if hasattr(m, "type") and m.type == "ai"]
        if ai_messages:
            print("-" * 70)
            print(f"Trợ lý: {ai_messages[-1].content}\n")
            print("-" * 70)

        for flag in ("knowledge_done", "specs_done", "generate_done", "evaluate_done"):
            if state.get(flag):
                print(f"{flag:<20} ====> TRUE")

    return state


if __name__ == "__main__":
    run()
