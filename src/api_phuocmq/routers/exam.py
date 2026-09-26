import uuid
from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from langchain_core.messages import HumanMessage, AIMessage
import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from src.api.session_store import SESSIONS_EXAM
from src.edu_exam.run_exam_v2 import build_initial_state   # nếu build_initial_state không export được do file run trực tiếp __main__, chuyển hàm này sang state_edu.py hoặc 1 file utils riêng

router = APIRouter(prefix="/api/exam", tags=["exam"])

EXAM_FLAGS = ["profile_complete", "knowledge_done", "matrix_done",
              "specs_done", "generate_done", "evaluate_done"]


@router.post("/session")
def create_session():
    session_id = str(uuid.uuid4())
    SESSIONS_EXAM[session_id] = build_initial_state()
    return {"session_id": session_id}


@router.post("/session/{session_id}/message")
async def send_message(session_id: str, body: dict, request: Request):
    state = SESSIONS_EXAM.get(session_id)
    if state is None:
        return {"error": "session không tồn tại"}

    state["messages"].append(HumanMessage(content=body["message"]))
    graph = request.app.state.exam_graph
    state = await run_in_threadpool(graph.invoke, state)
    SESSIONS_EXAM[session_id] = state

    ai_messages = [m for m in state["messages"] if isinstance(m, AIMessage)]
    return {
        "ai_message": ai_messages[-1].content if ai_messages else "",
        "flags":      {k: state.get(k, False) for k in EXAM_FLAGS},
        "exam_id":    state.get("exam_id"),   # có giá trị khi generate_done=True
        # thêm mới: FE cần nội dung đề để render, không chỉ exam_id
        "final_exam": state.get("final_exam") if state.get("evaluate_done") else None,
    }


@router.get("/session/{session_id}/state")
def get_session_state(session_id: str):
    """Debug: xem toàn bộ state hiện tại của session — bỏ hoặc khóa quyền khi lên production."""
    state = SESSIONS_EXAM.get(session_id)
    if state is None:
        return {"error": "session không tồn tại"}
    return {k: v for k, v in state.items() if k != "messages"}   # messages chứa object langchain, không serialize trực tiếp qua JSON mặc định