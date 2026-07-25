import sys, os, asyncio
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
from src.clients.llm import LLMClient
from src.clients.embedding import embeddings_qa
from src.configs import env_config
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever

load_dotenv()

EXIT_KEYWORDS = {"menu", "đổi chức năng", "doi chuc nang", "quay lại", "quay lai"}
def _init_shared():
    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)
    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="documents",
        top_k=10,
    )
    return llm_client, retriever


async def run_qa_mode(llm_client, retriever):
    from src.edu_qa.graph import build_qa_graph
    from src.edu_qa.state import QAState, ChatTurn

    graph = build_qa_graph(llm_client, retriever)
    chat_history: list[ChatTurn] = []

    while True:
        user_input = input("Học sinh: ").strip()
        if user_input.lower() == "quit":
            break
        if user_input.lower() in EXIT_KEYWORDS:
            print("Quay lại menu chọn chức năng...\n")
            return "menu"
        if not user_input:
            continue

        state = QAState(user_query=user_input, chat_history=chat_history)
        result_dict = await graph.ainvoke(state)
        result = QAState(**result_dict)

        print("-" * 70)
        print(f"Trợ lý: {result.final_answer}")
        print("-" * 70)

        chat_history.append(ChatTurn(user_query=user_input, final_answer=result.final_answer))


def run_exam_mode(llm_client, retriever):
    from src.edu_exam.run_exam import create_graph
    from langchain_core.messages import HumanMessage

    graph = create_graph(llm_client, retriever)

    state = {
        "messages": [], "student_profile": {}, "profile_complete": False,
        "detected_chapters": [], "retrieved_chunks": [], "retrieve_complete": False,
        "scope_chapters": {}, "scope_lessons": {}, "section_selected": False,
        "scored_chunks": [], "_pending_sections": [], "knowledge_profile": {},
        "knowledge_queue": None, "knowledge_pending": None, "knowledge_scores": {},
        "knowledge_done": False, "completed_build_knowlege": False, "exam_matrix": {},
        "question_specs": [], "specs_done": False, "generated_exam": [], "exam_memory": [],
        "generate_done": False, "exam_review": {}, "final_exam": [], "evaluate_done": False,
        "current_step": "", "error": None,
    }

    while True:
        user_input = input("Học sinh: ").strip()
        if user_input.lower() == "quit":
            break
        if user_input.lower() in EXIT_KEYWORDS:
            print("Quay lại menu chọn chức năng...\n")
            return "menu"
        if not user_input:
            continue

        state["messages"].append(HumanMessage(content=user_input))
        state = graph.invoke(state)

        ai_messages = [m for m in state["messages"] if hasattr(m, "type") and m.type == "ai"]
        if ai_messages:
            print("-" * 70)
            print(f"Trợ lý: {ai_messages[-1].content}\n")
            print("-" * 70)

        if state.get("evaluate_done"):
            break


def run_planning_mode(llm_client, retriever):
    print("Chức năng lộ trình học đang phát triển, chưa khả dụng.")


async def main():
    llm_client, retriever = _init_shared()

    while True:
        print("=" * 50)
        print("1. Hỏi đáp")
        print("2. Tạo bài kiểm tra")
        print("3. Tạo lộ trình học")
        print("=" * 50)

        mode = input("Chọn chức năng (1/2/3): ").strip()

        if mode == "1":
            signal = await run_qa_mode(llm_client, retriever)
        elif mode == "2":
            signal = run_exam_mode(llm_client, retriever)
        elif mode == "3":
            run_planning_mode(llm_client, retriever)
            signal = None
        else:
            print("Lựa chọn không hợp lệ.")
            continue

        if signal != "menu":
            break


if __name__ == "__main__":
    asyncio.run(main())