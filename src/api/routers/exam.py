import uuid
from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from langchain_core.messages import HumanMessage, AIMessage

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..","..")))


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
    }


@router.get("/session/{session_id}/state")
def get_session_state(session_id: str):
    """Debug: xem toàn bộ state hiện tại của session — bỏ hoặc khóa quyền khi lên production."""
    state = SESSIONS_EXAM.get(session_id)
    if state is None:
        return {"error": "session không tồn tại"}
    return {k: v for k, v in state.items() if k != "messages"}   # messages chứa object langchain, không serialize trực tiếp qua JSON mặc định


import json
from src.edu_qa.paths import TEST_EXAM_PROMPT_PATH


def _load_exam(exam_id: str):
    path = TEST_EXAM_PROMPT_PATH / f"{exam_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


@router.get("/{exam_id}")
def get_exam(exam_id: str):
    exam = _load_exam(exam_id)
    if exam is None:
        return {"error": "không tìm thấy đề"}
    questions = [{"id": q["id"], "question": q["question"], "options": q["options"]} for q in exam]
    return {"exam_id": exam_id, "total": len(questions), "questions": questions}


@router.post("/{exam_id}/submit")
def submit_exam(exam_id: str, body: dict):
    exam = _load_exam(exam_id)
    if exam is None:
        return {"error": "không tìm thấy đề"}

    answers = body.get("answers", {})   # {"1": "A", "2": "C"} — key JSON luôn là string
    detail, correct = [], 0
    for q in exam:
        qid = str(q["id"])
        your = answers.get(qid, "")
        is_correct = your == q.get("answer")
        correct += int(is_correct)
        detail.append({
            "id": q["id"], "question": q["question"], "options": q["options"],
            "your_answer": your, "correct_answer": q.get("answer"),
            "is_correct": is_correct, "giai_thich": q.get("giai_thich", ""),
        })

    return {"exam_id": exam_id, "score": correct, "total": len(exam), "detail": detail}