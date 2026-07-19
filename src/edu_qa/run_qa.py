import sys, os, asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dotenv import load_dotenv

from src.clients.llm import LLMClient
from src.configs import env_config
from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.edu_qa.state import QAState, ChatTurn
from src.edu_qa.graph import build_qa_graph

load_dotenv()


async def run():
    print("=" * 50)
    print("Hệ thống hỏi đáp Toán 10")
    print("=" * 50)
    print("Gõ 'quit' để thoát\n")

    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)

    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="documents",
        top_k=10,
    )

    graph = build_qa_graph(llm_client, retriever)
    chat_history: list[ChatTurn] = []

    while True:
        user_input = input("Học sinh: ").strip()
        if user_input.lower() == "quit":
            break
        if not user_input:
            continue

        state = QAState(user_query=user_input, chat_history=chat_history)
        result_dict = await graph.ainvoke(state)
        result = QAState(**result_dict)

        print("-" * 70)
        print(f"Trợ lý: {result.final_answer}")
        print("-" * 70)

        chat_history.append(ChatTurn(user_query=user_input, final_answer=result.final_answer))


if __name__ == "__main__":
    asyncio.run(run())