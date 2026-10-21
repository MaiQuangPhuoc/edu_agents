"""Giả lập edu_exam ở phía A2A: nhận HandoffMessage(request), trả HandoffMessage(result).
Sau này thay bằng edu_exam thật: chỉ cần đổi import handle_request ở entry_test.py."""
import json
from pathlib import Path
from src.state_plan import HandoffMessage
from src.entry_test_demo.entry_test_mock import create_mock_test


def _reply(ok: bool, **payload) -> dict:
    return HandoffMessage(sender="exam", receiver="roadmap", type="result",
                          payload={"ok": ok, **payload}).model_dump(mode="json")


def handle_request(msg: dict) -> dict:
    p = msg["payload"]
    try:
        info = create_mock_test(p["student_model"], count=p["num_questions"], output_dir=Path(p["out_dir"]))
    except ValueError as e:
        return _reply(False, error=str(e))
    questions = json.loads(Path(info["public_file"]).read_text(encoding="utf-8"))["questions"]
    return _reply(True, subject=info["subject"], key_file=info["key_file"], questions=questions)