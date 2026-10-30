"""Node bài test đầu vào: gửi yêu cầu (HandoffMessage) cho bên cấp đề, hiện đề và chờ đáp án."""
from pathlib import Path
from langchain_core.messages import AIMessage
from src.state_plan import PlanState, HandoffMessage
from src.entry_test_demo.mock_exam_agent import handle_request      # sau này: từ edu_exam

NUM_QUESTIONS = 20
OUT_ROOT = Path(__file__).resolve().parents[1] / "entry_test_demo" / "output"


def _show(questions: list[dict]) -> str:
    lines = [f"BÀI KIỂM TRA ĐẦU VÀO ({len(questions)} câu)"]
    for q in questions:
        lines.append(f"\nCâu {q['no']} (Chương {q['chapter_id']}): {q['question']}")
        lines += [f"  {k}. {v}" for k, v in q["options"].items()]
    lines.append("\nBạn làm xong gửi đáp án theo dạng 1-a, 2-c, 3-b, ... nhé.")
    return "\n".join(lines)


def entry_test_node(state: PlanState) -> dict:
    print(">>> [TEST] entry_test")
    sid = state.get("student_id", "unknown")
    payload = {"student_id": sid, "num_questions": NUM_QUESTIONS, "out_dir": str(OUT_ROOT / sid)}
    req = HandoffMessage(sender="roadmap", receiver="exam", type="request", payload=payload).model_dump(mode="json")
    res = handle_request({**req, "payload": {**payload, "student_model": state["student_model"]}})
    inbox = list(state.get("inbox", [])) + [req, {**res, "payload": {k: v for k, v in res["payload"].items() if k != "questions"}}]

    p = res["payload"]
    if not p["ok"]:
        return {"inbox": inbox, "roadmap_status": "entry_test_failed", "messages": [AIMessage(
            content=f"Mình chưa tạo được bài test đầu vào ({p.get('error', 'lỗi không rõ')}). Bạn nhắn \"thử lại\" nhé.")]}
    return {"inbox": inbox, "roadmap_status": "awaiting_test_answers",
            "entry_test": {"subject": p["subject"], "key_file": p["key_file"], "questions": [{k: q[k] for k in ("no", "chapter_id", "question", "options") if k in q} for q in p["questions"]]},
            "messages": [AIMessage(content=_show(p["questions"]))]}