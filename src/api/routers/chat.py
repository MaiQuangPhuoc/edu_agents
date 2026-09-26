import uuid
from fastapi import APIRouter, Request
from src.api.session_store import SESSIONS_QA
from src.edu_qa.state import QAState

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/session")
def create_session():
    session_id = str(uuid.uuid4())
    SESSIONS_QA[session_id] = QAState(user_query="").model_dump()
    return {"session_id": session_id}


@router.post("/session/{session_id}/message")
async def send_message(session_id: str, body: dict, request: Request):
    state_dict = SESSIONS_QA.get(session_id)
    if state_dict is None:
        return {"error": "session không tồn tại"}

    state = QAState(**state_dict)
    state.user_query = body["message"]

    graph = request.app.state.qa_graph
    result_dict = await graph.ainvoke(state)
    state = QAState(**result_dict)
    SESSIONS_QA[session_id] = state.model_dump()

    return {"final_answer": state.final_answer, "suggestions": state.suggestions}