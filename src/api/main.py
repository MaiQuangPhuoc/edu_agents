import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from contextlib import asynccontextmanager
from fastapi import FastAPI
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.clients.llm import LLMClient
from src.clients.embedding import embeddings_qa
from src.configs import env_config
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.edu_exam.graph_exam_v2 import create_graph as create_exam_graph
from src.edu_qa.graph import build_graph as build_qa_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)
    retriever  = VectorStoreRetriever(
        url=env_config.qdrant_url, api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa, collection_name="doc_final",
        tools_collection_name="tools", top_k=10,
    )
    app.state.llm_client  = llm_client
    app.state.retriever   = retriever
    app.state.exam_graph  = create_exam_graph(llm_client, retriever)
    app.state.qa_graph    = build_qa_graph(retriever, llm_client)
    print(">>> đã khởi tạo llm_client, retriever, exam_graph, qa_graph")
    yield


app = FastAPI(title="EDUAGENT API", lifespan=lifespan)


from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

from src.api.routers import exam, chat, pages   # noqa: E402
app.include_router(pages.router)
app.include_router(exam.router)
app.include_router(chat.router)


# from src.api_phuocmq.routers import exam, chat   # noqa: E402 (import sau khi app đã định nghĩa, tránh vòng lặp import)
# app.include_router(exam.router)
# app.include_router(chat.router)