import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.messages import HumanMessage, AIMessage
from src.state_edu import ExamState, CollectInfoResponse
from src.clients.llm import LLMClient
from pathlib import Path
from src.edu_qa.paths import COLLECT_INFO_PROMPT_PATH


SYSTEM_PROMPT = COLLECT_INFO_PROMPT_PATH.read_text(encoding="utf-8")

REQUIRED_FIELDS = ["mon_hoc", "khoi_lop", "pham_vi_kiem_tra"]

HISTORY_TURN_LIMIT = 5   # chỉ giữ 5 lượt hỏi-đáp gần nhất, đủ mạch hội thoại mà không phình prompt


def _merge_profile(existing: dict, new) -> dict:
    merged = dict(existing)
    for field, value in new.model_dump().items():
        if value is not None:
            merged[field] = value
    return merged


def _is_complete(profile: dict) -> bool:
    return all(profile.get(k) is not None for k in REQUIRED_FIELDS)


def _format_known_profile(profile: dict) -> str:
    """Tóm tắt field đã biết — thay thế cho việc phải đọc lại toàn bộ history để suy ra field nào còn thiếu."""
    if not profile:
        return "Chưa có thông tin nào."
    return "\n".join(f"- {k}: {v}" for k, v in profile.items() if v is not None)


def _recent_history(messages: list, turn_limit: int) -> list:
    """Chỉ lấy N lượt hỏi-đáp gần nhất (1 lượt = 1 Human + 1 AI), giới hạn token."""
    trimmed = []
    turns = 0
    for m in reversed(messages):
        trimmed.append(m)
        if isinstance(m, HumanMessage):
            turns += 1
        if turns >= turn_limit:
            break
    return list(reversed(trimmed))


def collect_info(state: ExamState, llm_client: LLMClient) -> dict:
    print("=========================== collect_info ===========================\n"*2)
    profile_complete = state.get("profile_complete", False)
    if profile_complete:
        print("collect info xonggggg")
        return {}
    
    messages         = state.get("messages", [])
    student_profile  = state.get("student_profile", {})
    recent = _recent_history(messages, HISTORY_TURN_LIMIT)
    history = [
        {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content}
        for m in recent
    ]

    profile_context = _format_known_profile(student_profile)
    system_prompt = (
        SYSTEM_PROMPT
        + f"\n\n## Thông tin đã thu thập được đến hiện tại:\n{profile_context}"
        + "\n\nChỉ hỏi các field còn thiếu, không hỏi lại field đã có."
    )

    structured_llm = llm_client._llm.with_structured_output(CollectInfoResponse)

    result = None
    for attempt in range(3):
        try:
            result = structured_llm.invoke([
                {"role": "system", "content": system_prompt},
                *history,
            ])
            break
        except Exception as e:
            print(f"[collect_info] attempt {attempt} lỗi: {e}")

    if result is None:
        # fallback: hỏi lại đơn giản, không crash cả graph
        return {
            "messages": [AIMessage(content="Xin lỗi, bạn có thể nhắc lại thông tin rõ hơn được không?")],
            "student_profile": student_profile,
            "profile_complete": False,
            "current_step": "collect_info",
        }

    new_profile = _merge_profile(student_profile, result.profile)
    print(f"new_profile: {new_profile}")
    all_fields_filled = _is_complete(new_profile)
    complete = all_fields_filled and result.is_confirmed   # ← chỉ complete khi ĐỦ field VÀ đã xác nhận

    print(f"complete: {complete}")
    return {
        "messages": [AIMessage(content=result.reply)],
        "student_profile": new_profile,
        "profile_complete": complete,
        "current_step": "collect_info",
    }