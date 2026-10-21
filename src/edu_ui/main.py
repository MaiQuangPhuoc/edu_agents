"""EDUAGENT UI standalone FastAPI entrypoint.
Run at repository root: uvicorn src.edu_ui.main:app --reload --port 8001
Optionally configure EDU_QA_API_URL to an existing QA FastAPI service.
"""
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel, Field
import httpx

BASE = Path(__file__).resolve().parent
app = FastAPI(title="EDUAGENT UI")
app.mount("/ui-static", StaticFiles(directory=BASE / "static"), name="ui-static")
templates = Jinja2Templates(directory=str(BASE / "templates"))
QA_URL = os.getenv("EDU_QA_API_URL", "http://127.0.0.1:8000").rstrip("/")

class ChatInput(BaseModel):
    session_id: str | None = None
    message: str = Field(min_length=1, max_length=15000)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html", context={})

@app.post("/api/ui/chat")
async def chat(body: ChatInput):
    """Proxy for existing src.api QA endpoints. No invented RAG sources."""
    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            sid = body.session_id
            if not sid:
                create = await client.post(f"{QA_URL}/api/chat/session")
                create.raise_for_status()
                sid = create.json()["session_id"]
            res = await client.post(
                f"{QA_URL}/api/chat/session/{sid}/message", json={"message": body.message}
            )
            res.raise_for_status()
            result = res.json()
            if result.get("error"):
                raise HTTPException(status_code=422, detail=result["error"])
            # Existing QA returns final_answer and suggestions; retrieval sources aren't exposed yet.
            return {"session_id": sid, "answer": result.get("final_answer", ""),
                    "suggestions": result.get("suggestions", []),
                    "sources": result.get("sources", [])}
    except httpx.HTTPError as ex:
        raise HTTPException(status_code=503, detail="Backend QA chưa sẵn sàng. Hãy chạy src.api.main trước.") from ex

@app.get("/api/ui/health")
def health():
    return {"status": "ok", "qa_backend": QA_URL}


# Book-name registration endpoints (without RAG ingestion)
from src.edu_ui.book_api import router as book_router
app.include_router(book_router)

@app.get("/documents", response_class=HTMLResponse)
def documents_page(request: Request):
    return templates.TemplateResponse(request=request, name="documents.html", context={})

# Exams UI and data endpoints
from src.edu_ui.exam_api import router as exam_router
app.include_router(exam_router)

@app.get("/exams", response_class=HTMLResponse)
def exams_page(request: Request):
    return templates.TemplateResponse(request=request, name="exams.html", context={})

# Roadmap UI (read-only until Planning Agent persistence is connected)
from src.edu_ui.roadmap_api import router as roadmap_router
app.include_router(roadmap_router)

@app.get("/roadmap", response_class=HTMLResponse)
def roadmap_page(request: Request):
    return templates.TemplateResponse(request=request, name="roadmap.html", context={})
