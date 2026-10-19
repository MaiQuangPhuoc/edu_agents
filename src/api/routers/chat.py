import uuid
from time import perf_counter

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from src.api.session_store import SESSIONS_QA
from src.edu_qa.state import QAState

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


@router.post("/session")
def create_session():
    session_id = str(uuid.uuid4())
    SESSIONS_QA[session_id] = QAState(user_query="").model_dump()
    return {"session_id": session_id}


@router.post("/session/{session_id}/message")
async def send_message(session_id: str, body: ChatMessage, request: Request):
    state_dict = SESSIONS_QA.get(session_id)
    if state_dict is None:
        raise HTTPException(status_code=404, detail="Cuộc trò chuyện không tồn tại hoặc đã hết hạn.")

    state = QAState(**state_dict)
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Tin nhắn không được để trống.")
    state.user_query = message

    graph = request.app.state.qa_graph
    started_at = perf_counter()
    result_dict = await graph.ainvoke(state)
    generation_time = perf_counter() - started_at
    state = QAState(**result_dict)
    SESSIONS_QA[session_id] = state.model_dump()

    return {
        "final_answer": state.final_answer,
        "suggestions": state.suggestions,
        "generation_time_seconds": round(generation_time, 3),
    }