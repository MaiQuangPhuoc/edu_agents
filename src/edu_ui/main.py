"""EDUAGENT UI standalone FastAPI entrypoint.
Run at repository root: uvicorn src.edu_ui.main:app --reload --port 8001
QA, Exam and Planning graphs are lazy-loaded by workflow_api.
The retired QA-only endpoint reports stale browser bundles explicitly.
"""
from pathlib import Path
from contextlib import asynccontextmanager, suppress
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel, Field

from dotenv import load_dotenv
BASE = Path(__file__).resolve().parent
load_dotenv(BASE.parents[1] / ".env", encoding="utf-8-sig", override=False)
@asynccontextmanager
async def ui_lifespan(app):
    from src.edu_ui.workflow_engine import engine
    warmup = asyncio.create_task(engine.warmup())
    try:
        yield
    finally:
        if not warmup.done():
            warmup.cancel()
        with suppress(asyncio.CancelledError):
            await warmup

app = FastAPI(title="EDUAGENT UI", lifespan=ui_lifespan)
app.mount("/ui-static", StaticFiles(directory=BASE / "static"), name="ui-static")
templates = Jinja2Templates(directory=str(BASE / "templates"))

class ChatInput(BaseModel):
    session_id: str | None = None
    message: str = Field(min_length=1, max_length=15000)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="chat.html", context={"active_page": "chat"}
    )

@app.post("/api/ui/chat")
async def legacy_chat(body: ChatInput):
    # A stale browser bundle must not silently use the retired QA-only proxy.
    raise HTTPException(status_code=409, detail=(
        "Trình duyệt đang dùng giao diện chat cũ. Nhấn Ctrl+F5; nếu vẫn lỗi, "
        "cập nhật đủ chat.html, chat.js và workflow.js trong src/edu_ui."
    ))

@app.get("/api/ui/health")
def health():
    return {"status": "ok", "ui_version": "workflow-ui-3",
            "workflow_api": "/api/ui/workflows", "project_root": str(BASE.parents[1])}

@app.middleware("http")
async def fresh_ui_assets(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/ui-static/") or response.headers.get("content-type", "").startswith("text/html"):
        response.headers["Cache-Control"] = "no-store, max-age=0"
    return response


# Book-name registration endpoints (without RAG ingestion)
from src.edu_ui.book_api import router as book_router
app.include_router(book_router)

@app.get("/documents", response_class=HTMLResponse)
def documents_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="documents.html", context={"active_page": "documents"}
    )

# Exams UI and data endpoints
from src.edu_ui.exam_api import router as exam_router
app.include_router(exam_router)

@app.get("/exams", response_class=HTMLResponse)
def exams_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="exams.html", context={"active_page": "exams"}
    )

# Roadmap UI (read-only until Planning Agent persistence is connected)
from src.edu_ui.roadmap_api import router as roadmap_router
app.include_router(roadmap_router)

@app.get("/roadmap", response_class=HTMLResponse)
def roadmap_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="study.html", context={"active_page": "roadmap"}
    )

# Student profile uses the canonical planning StudentModel schema.
from src.edu_ui.profile_api import router as profile_router
app.include_router(profile_router)

@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="profile.html", context={"active_page": "profile"}
    )


# Real graph workflows are lazy-loaded; this UI needs only one server process.
from src.edu_ui.workflow_api import router as workflow_router
app.include_router(workflow_router)

@app.get("/study", response_class=HTMLResponse)
def study_page(request: Request):
    return templates.TemplateResponse(request=request, name="study.html", context={"active_page": "chat"})
