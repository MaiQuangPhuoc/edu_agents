# from xxlimited import new

from dotenv import load_dotenv
load_dotenv()
import logging
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from src.edu_planning.entry_test import entry_test_node
from src.edu_planning.entry_grade import entry_grade_node
from src.clients.llm import LLMClient
from src.configs import env_config
from src.edu_planning.collect_student_model import collect_student_model
# import trong hàm để chế độ collect không phải nạp mô hình embedding/reranker
from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.edu_planning.roadmap_graph import make_roadmap_graph
from src.edu_planning.student_store import load_student_model
from src.edu_planning.query_builder import build_queries
from pathlib import Path
from datetime import datetime
from src.edu_exam.exam_for_session import run_for_enabled_session

logging.basicConfig(level=logging.INFO)


# MODE = "collect" 
# MODE = "plan" 
MODE = "full"   
STUDENT_ID = "hs_006"


CHAT_START = datetime.now()
CHAT_FILE = Path(__file__).resolve().parent / (
    f"{CHAT_START:%Y-%m-%d_%H-%M-%S}.md"
)

def log_chat(role: str, message: str):
    timestamp = datetime.now().strftime("%M:%S")

    with CHAT_FILE.open("a", encoding="utf-8") as f:
        f.write(f"### [{timestamp}] {role}\n\n{message}\n\n")


def show_new_bot_messages(out):
    msgs = out["messages"]
    last_human = max((i for i, m in enumerate(msgs) if isinstance(m, HumanMessage)), default=-1)
    for m in msgs[last_human + 1:]:
        if isinstance(m, AIMessage):
            print("\nBot:", m.content)
            log_chat("Bot", m.content)

def _apply(state, out):
    msgs = out.pop("messages", [])
    state["messages"].extend(msgs)
    state.update(out)
    for m in msgs:
        print("\nBot:", m.content)
        log_chat("Bot", m.content)


def run_entry(state, llm_client):
    _apply(state, entry_test_node(state))
    while state.get("roadmap_status") == "awaiting_test_answers":
        text = input("\nĐáp án của bạn: ").strip()
        log_chat("Học sinh", text)
        state["messages"].append(HumanMessage(content=text))
        _apply(state, entry_grade_node(state, llm_client))
        

def run_collect(llm_client):
    state = {
        "student_id": STUDENT_ID,
        "messages": []
    }

    while not state.get("model_done"):
        # Bot xử lý và phản hồi
        out = collect_student_model(state, llm_client)
        new_messages = out.pop("messages", [])

        state["messages"].extend(new_messages)
        state.update(out)

        # Hiển thị và lưu tin nhắn Bot
        for msg in new_messages:
            if isinstance(msg, AIMessage):
                print("\nBot:", msg.content)
                log_chat("Bot", msg.content)

        if state.get("model_done"):
            break

        # Nhận và lưu tin nhắn học sinh
        user_input = input("\nBạn: ").strip()

        if not user_input:
            continue

        log_chat("Học sinh", user_input)
        state["messages"].append(
            HumanMessage(content=user_input)
        )
    run_entry(state, llm_client)
    print("\n>>> Hồ sơ đã lưu. Truy vấn tra cứu:")

    for q in state.get("search_queries", []):
        print("  -", q)

def run_plan(llm_client):
    model = load_student_model(STUDENT_ID)
    if not model:
        print(f"Chưa có hồ sơ {STUDENT_ID}. Hãy chạy MODE='collect' trước.")
        return
    queries = build_queries(model)
    print(">>> Truy vấn tham khảo:")
    for q in queries:
        print("  -", q)

    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",
        top_k=10,
    )
    graph = make_roadmap_graph(retriever, llm_client, checkpointer=MemorySaver())
    cfg = {"configurable": {"thread_id": STUDENT_ID}}

    # bỏ qua collect + bài test: nạp sẵn hồ sơ, đánh dấu đã xong
    out = graph.invoke({
        "student_id": STUDENT_ID, "messages": [],
        "student_model": model, "model_done": True,
        "entry_done": True, "search_queries": queries,
    }, cfg)
    show_new_bot_messages(out)
    while out.get("roadmap_status") not in ("approved", "path_ready", "path_failed"):
        text = input("\nBạn: ").strip()
        if not text:
            continue

        log_chat("Học sinh", text)
        out = graph.invoke({"messages": [HumanMessage(content=text)]}, cfg)
        show_new_bot_messages(out)

def run_full(llm_client):


    print(">>> 1. =============================== tạo retriever =============================== ")
    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",     # collection chung 3 môn, lọc theo metadata["subject"]
        top_k=10,
        # reranker_model="BAAI/bge-reranker-base",   # bỏ comment nếu chương trình dừng khi nạp reranker
    )
    print(">>> 2. =============================== tạo graph =============================== ")
    graph = make_roadmap_graph(retriever, llm_client, checkpointer=MemorySaver())
    cfg = {"configurable": {"thread_id": STUDENT_ID}}

    print(">>> 3. ===============================  bắt đầu hội thoại =============================== ")
    out = graph.invoke({"student_id": STUDENT_ID, "messages": []}, cfg)
    show_new_bot_messages(out)
    while out.get("roadmap_status") != "path_ready":
        text = input("\nBạn: ").strip()
        if not text:
            continue

        log_chat("Học sinh", text)
        out = graph.invoke({"messages": [HumanMessage(content=text)]}, cfg)
        show_new_bot_messages(out)
    print(f" ================================ bài tập cho buổi chi tiết ================================ "*2)
    print("\n\n")
    run_for_enabled_session(out, llm_client, retriever)


if __name__ == "__main__":
    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)
    print(">>> =============================== LLMClient xong  =============================== ")
    # run_collect(llm_client) if MODE == "collect" else run_full(llm_client)
    {"collect": run_collect, "plan": run_plan, "full": run_full}[MODE](llm_client)