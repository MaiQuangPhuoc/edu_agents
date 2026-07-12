from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class QAState(TypedDict):
    messages: Annotated[list, add_messages]

    retrieved_chunks: list[dict]

    clarify_question: Optional[str]
    awaiting_user: bool

    answer: str


def get_last_question(state: "QAState") -> str:
    """Lấy nội dung câu hỏi mới nhất từ messages (HumanMessage cuối cùng)."""
    for msg in reversed(state.get("messages", [])):
        if getattr(msg, "type", None) == "human":
            return msg.content
    return ""
