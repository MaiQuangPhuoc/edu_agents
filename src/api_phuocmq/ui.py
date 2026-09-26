import uuid
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.concurrency import run_in_threadpool
from langchain_core.messages import HumanMessage, AIMessage
import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.api_phuocmq.session_store import SESSIONS_EXAM, SESSIONS_QA
from src.edu_qa.state import QAState
from src.edu_exam.run_exam_v2 import build_initial_state

router = APIRouter(tags=["ui"])


# ---------- trang chủ ----------

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("home.html", {"request": request})


# ---------- luồng hỏi đáp (edu_qa) ----------

@router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    templates = request.app.state.templates
    session_id = request.cookies.get("qa_session_id")
    if not session_id or session_id not in SESSIONS_QA:
        session_id = str(uuid.uuid4())
        SESSIONS_QA[session_id] = QAState(user_query="").model_dump()

    resp = templates.TemplateResponse("chat.html", {"request": request, "session_id": session_id})
    resp.set_cookie("qa_session_id", session_id, httponly=True)
    return resp


@router.post("/chat/{session_id}/message", response_class=HTMLResponse)
async def chat_message(session_id: str, request: Request, message: str = Form(...)):
    templates = request.app.state.templates
    state_dict = SESSIONS_QA.get(session_id)
    if state_dict is None:
        return HTMLResponse('<div class="text-red-500 text-sm px-1">Phiên đã hết hạn, vui lòng tải lại trang.</div>')

    state = QAState(**state_dict)
    state.user_query = message

    graph = request.app.state.qa_graph
    result_dict = await graph.ainvoke(state)
    state = QAState(**result_dict)
    SESSIONS_QA[session_id] = state.model_dump()

    return templates.TemplateResponse("_chat_turn.html", {
        "request": request,
        "session_id": session_id,
        "user_message": message,
        "final_answer": state.final_answer,
        "suggestions": state.suggestions or [],
    })


# ---------- luồng tạo đề (edu_exam) ----------

@router.get("/exam", response_class=HTMLResponse)
def exam_page(request: Request):
    templates = request.app.state.templates
    session_id = request.cookies.get("exam_session_id")
    if not session_id or session_id not in SESSIONS_EXAM:
        session_id = str(uuid.uuid4())
        SESSIONS_EXAM[session_id] = build_initial_state()

    resp = templates.TemplateResponse("exam.html", {"request": request, "session_id": session_id})
    resp.set_cookie("exam_session_id", session_id, httponly=True)
    return resp


@router.post("/exam/{session_id}/message", response_class=HTMLResponse)
async def exam_message(session_id: str, request: Request, message: str = Form(...)):
    templates = request.app.state.templates
    state = SESSIONS_EXAM.get(session_id)
    if state is None:
        return HTMLResponse('<div class="text-red-500 text-sm px-1">Phiên đã hết hạn, vui lòng tải lại trang.</div>')

    state["messages"].append(HumanMessage(content=message))
    graph = request.app.state.exam_graph
    state = await run_in_threadpool(graph.invoke, state)
    SESSIONS_EXAM[session_id] = state

    ai_messages = [m for m in state["messages"] if isinstance(m, AIMessage)]
    return templates.TemplateResponse("_exam_turn.html", {
        "request": request,
        "session_id": session_id,
        "user_message": message,
        "ai_message": ai_messages[-1].content if ai_messages else "",
        "evaluate_done": state.get("evaluate_done", False),
        "final_exam": state.get("final_exam"),
        "exam_id": state.get("exam_id"),
    })