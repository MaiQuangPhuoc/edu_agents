import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from src.edu_qa.qa_state import QAState, get_last_question
from src.clients.llm import LLMClient
from src.edu_qa.tools.sympy_qa_tools import QA_TOOLS

AGENT_PROMPT_PATH = Path(r'D:\VKU\Nam_4\ky_I\computer_vision\EDUAGENT\prompt_edu\prompt\qa_answer_agent.txt')


# ── Xử lý dữ liệu TRƯỚC khi đưa vào agent ──────────────────────────────────

def _format_chunks(chunks: list) -> str:
    """Chuẩn hóa retrieved_chunks thành text sạch cho agent đọc.
    Đây là bước xử lý dữ liệu, KHÔNG phải quyết định thay agent.
    """
    if not chunks:
        return "Không có tài liệu tham chiếu cho câu hỏi này."
    return "\n---\n".join(c["content"] for c in chunks)


def _build_input_message(question: str, chunks_text: str) -> HumanMessage:
    return HumanMessage(content=(
        f"Câu hỏi của học sinh:\n{question}\n\n"
        f"Tài liệu tham chiếu (nếu có nội dung liên quan, ưu tiên dùng để "
        f"xác định công thức/quy tắc áp dụng):\n{chunks_text}"
    ))


# ── Xử lý dữ liệu SAU khi agent chạy xong ──────────────────────────────────

def _extract_final_answer(agent_messages: list) -> str:
    """Lấy câu trả lời cuối cùng agent sinh ra sau khi đã gọi tool
    (nếu có) và tự quyết định đã đủ thông tin để trả lời.
    """
    ai_texts = [
        m.content for m in agent_messages
        if isinstance(m, AIMessage) and m.content
    ]
    return ai_texts[-1] if ai_texts else "Xin lỗi, hệ thống chưa tạo được câu trả lời."


def _extract_tools_used(agent_messages: list) -> list:
    """Chỉ để log/debug — xem agent đã tự chọn gọi tool nào, không dùng
    để rẽ nhánh logic.
    """
    return [
        m.name for m in agent_messages
        if getattr(m, "type", None) == "tool"
    ]


# ── Node chính ───────────────────────────────────────────────────────────────

def answer_node(state: QAState, llm_client: LLMClient) -> dict:
    print(">>> [Node] answer_node")

    question    = get_last_question(state)
    chunks      = state.get("retrieved_chunks", [])
    chunks_text = _format_chunks(chunks)

    system_prompt = AGENT_PROMPT_PATH.read_text(encoding="utf-8")

    # Agent được cấp toàn bộ tool sẵn có, TỰ quyết định có gọi hay không,
    # gọi tool nào, gọi mấy lần — không có logic if/else nào áp đặt trước.
    agent = create_react_agent(
        model=llm_client._llm,
        tools=QA_TOOLS,
        prompt=system_prompt,
    )

    input_message = _build_input_message(question, chunks_text)
    result = agent.invoke({"messages": [input_message]})

    agent_messages = result["messages"]
    answer = _extract_final_answer(agent_messages)

    tools_used = _extract_tools_used(agent_messages)
    print(f">>> answer_node: tools_used={tools_used}")

    return {
        "messages": [AIMessage(content=answer)],
        "answer":   answer,
    }
