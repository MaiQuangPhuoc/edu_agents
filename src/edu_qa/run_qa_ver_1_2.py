import sys, os, asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dotenv import load_dotenv

from src.clients.llm import LLMClient
from src.configs import env_config
from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.edu_qa.state import QAState
from src.edu_qa.graph import build_graph

load_dotenv()

# lịch sử nước Việt Nam ai là vua đặt tên nước là Đại cồ việt
# trong toán học mệnh đề có ý nghĩa gì , có các loại mệnh đề nào

async def run():
    print("=" * 50)
    print("Hệ thống hỏi đáp Toán - Văn - Sử lớp 10 (EDUAGENT)")
    print("=" * 50)
    print("Gõ 'q' để thoát\n")

    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)

    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",
        tools_collection_name="tools",
        top_k=10,
        enable_colbert_prefilter=True,
        colbert_model="colbert-ir/colbertv2.0",
    )

    graph = build_graph(retriever, llm_client)

    # state được giữ nguyên xuyên suốt phiên chat, chat_history tự ghi bên trong graph
    state = QAState(user_query="")

    while True:
        user_input = input("Học sinh: ").strip()
        if user_input.lower() == "q":
            break
        if not user_input:
            continue

        state.user_query = user_input
        result_dict = await graph.ainvoke(state)
        state = QAState(**result_dict)

        print("-" * 70)
        print(f"Trợ lý: {state.final_answer}")
        if state.suggestions:
            print("\nGợi ý câu hỏi tiếp theo:")
            for i, sug in enumerate(state.suggestions, start=1):
                print(f"  {i}. {sug}")
        print("-" * 70)


if __name__ == "__main__":
    asyncio.run(run())