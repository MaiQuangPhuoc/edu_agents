import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.edu_qa.state import QAState, ChatTurn
MAX_HISTORY_TURNS = 5

def build_history_text(state: QAState) -> str:
    """Tạo chuỗi lịch sử hội thoại từ state.chat_history, dùng chung cho mọi prompt cần ngữ cảnh."""
    recent = state.chat_history[-MAX_HISTORY_TURNS:]
    if not recent:
        return "Không có lịch sử, đây là câu hỏi đầu tiên."

    parts = []
    for i, turn in enumerate(recent, start=1):
        parts.append(f"Lượt {i}:\nHọc sinh hỏi: {turn.user_query}\nHệ thống trả lời: {turn.final_answer}")
    return "\n\n".join(parts)


def append_chat_turn(state: QAState) -> QAState:
    """Ghi lượt hỏi-đáp hiện tại vào chat_history, gọi sau khi state.final_answer đã có giá trị."""
    if state.final_answer is None:
        raise ValueError("Không thể append ChatTurn khi final_answer chưa có giá trị")

    state.chat_history.append(
        ChatTurn(user_query=state.user_query, final_answer=state.final_answer)
    )
    return state