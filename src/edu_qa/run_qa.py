import sys, os, asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dotenv import load_dotenv
import re 
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
        # user_input = re.sub(r"#.*", "", user_input).strip()  # Loại bỏ phần chú thích bắt đầu bằng #
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

# trình bày tổng quan về mệnh đề tập hợp bằng 5 ý cốt lõi và cho 3 ví dụ giải thích các ví dụ đó 
#  [
#   {
#     "question": "Cho tập hợp A={1,2,3,4,5} và B={3,4,5,6,7}. Hãy tính A ∩ B.",
#     "answer": "{3,4,5}"
#   },
#   {
#     "question": ".",
#     "answer": "{1,3,5}"
#   },
#   {
#     "question": "Xét mệnh đề P: '5 là số nguyên tố' và Q: '8 là số chẵn'. Hãy xác định giá trị chân lý của mệnh đề P ⇒ Q.",
#     "answer": "Đúng"
#   },
#   {
#     "question": "Biểu diễn miền nghiệm của bất phương trình bậc nhất hai ẩn x + y ≤ 4. Kiểm tra điểm M(1;2) có thuộc miền nghiệm hay không.",
#     "answer": "Có"
#   },
#   {
#     "question": "Cho hệ bất phương trình: x+y≤5 và x−y≥1. Kiểm tra điểm A(3;1) có là nghiệm của hệ hay không.",
#     "answer": "Có"
#   },
#   {
#     "question": "Cho hàm số y=x²−4x+3. Tính giá trị của hàm số tại x=2.",
#     "answer": "-1"
#   }
# ]

# Cho:A là tập hợp các số nguyên x thỏa mãn: −2≤x≤5 , B là tập hợp các số nguyên x thỏa mãn: x^2 < 20, Hãy xác định tập hợp: (A∪B)∖(A∩B)
# {−4,−3}

# Một quả bóng được đá lên cao, độ cao của bóng theo thời gian được mô tả bởi: h(t)=−5t^2+20t+1
# (với h tính bằng mét) , Hỏi quả bóng đạt độ cao lớn nhất bằng bao nhiêu mét?
# Đáp án: 21 mét.Cho tập hợp A={1,2,3,4,5} và B={2,4}. Hãy tính phần bù của B trong A