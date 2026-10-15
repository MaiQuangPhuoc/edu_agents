# from langchain_core.messages import AIMessage, HumanMessage
# from langgraph.checkpoint.memory import MemorySaver

import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
load_dotenv()

from src.clients.llm import LLMClient
from src.clients.embedding import embeddings_qa
from src.configs import env_config
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
# from src.edu_planning.roadmap_graph import make_roadmap_graph
print(">>> 1. import xong")   

llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)
print(">>> 2. LLMClient xong")  
# Collection chung cho cả 3 môn (Toán/Văn/Sử), lọc theo metadata["subject"] ở tầng retriever
retriever = VectorStoreRetriever(
    url=env_config.qdrant_url,
    api_key=env_config.qdrant_api_key,
    embeddings=embeddings_qa,
    collection_name="doc_final",
    tools_collection_name="tools",     # ← thêm dòng này
    top_k=10,
)
print(">>> 3. retriever xong")     


# # retriever, llm_client: khởi tạo như ở run_exam_v2.py / graph.py
# graph = make_roadmap_graph(retriever, llm_client, checkpointer=MemorySaver())
# print(">>> 4. graph xong")     


# cfg = {"configurable": {"thread_id": "hs_001"}}
# print(">>> 5. bắt đầu invoke")    

# def show_new_bot_messages(out):
#     msgs = out["messages"]
#     last_human = max((i for i, m in enumerate(msgs) if isinstance(m, HumanMessage)), default=-1)
#     for m in msgs[last_human + 1:]:
#         if isinstance(m, AIMessage):
#             print("\nBot:", m.content)


# out = graph.invoke({"student_id": "hs_001", "messages": []}, cfg)
# show_new_bot_messages(out)

# while out.get("roadmap_status") != "approved":
#     out = graph.invoke({"messages": [HumanMessage(content=input("\nBạn: "))]}, cfg)
#     show_new_bot_messages(out)