"""Chấm bài test đầu vào: chuẩn hóa đáp án học sinh gõ về dạng 1-a, so với file đáp án, cập nhật hồ sơ."""
import re, json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import datetime
from pathlib import Path
from langchain_core.messages import AIMessage, HumanMessage
from src.state_plan import PlanState

STRONG, WEAK = 0.7, 0.5      # tỉ lệ đúng của chương: >= STRONG là mạnh, < WEAK là yếu
FULL_CONF = 5                # chương có từ chừng này câu trở lên thì độ tin cậy = 1.0

_ANS = re.compile(r"(\d+)\s*[-–—:.)]*\s*([A-Da-d])(?![A-Za-z])")


def parse_answers(text: str) -> dict[int, str]:
    """"1A", "1 - A", "1-a", "2. b", "3)c" -> {1: "a", 2: "b", 3: "c"}; câu lặp thì lấy lần cuối."""
    return {int(n): a.lower() for n, a in _ANS.findall(text or "")}


def normalize_answers(ans: dict[int, str]) -> str:
    return ", ".join(f"{n}-{a}" for n, a in sorted(ans.items()))


def grade(key: list[dict], ans: dict[int, str]) -> dict:
    by_ch, right = {}, 0
    for q in key:
        c = by_ch.setdefault(q["chapter_id"], {"total": 0, "correct": 0})
        c["total"] += 1
        if ans.get(q["no"]) == q["answer"].lower():
            c["correct"] += 1
            right += 1
    return {"total": len(key), "correct": right, "answered": sum(1 for q in key if q["no"] in ans), "chapters": by_ch}


def update_profile(sm: dict, subject: str, result: dict) -> dict:
    """Ghi muc_nam (0-1), do_tin_cay, diem_manh/diem_yeu của các chương đã test; đặt da_test_dau_vao."""
    now = datetime.now().isoformat()
    for nl in sm.get("nang_luc", []):
        if nl.get("mon_hoc") != subject:
            continue
        tested = result["chapters"]
        nl["chu_de"] = [c for c in nl.get("chu_de", []) if c["chapter_id"] not in tested]
        nl["diem_manh"] = [c for c in nl.get("diem_manh", []) if c not in tested]
        nl["diem_yeu"] = [c for c in nl.get("diem_yeu", []) if c not in tested]
        for cid, s in tested.items():
            ratio = s["correct"] / s["total"]
            nl["chu_de"].append({"chapter_id": cid, "lesson": "", "muc_nam": round(ratio, 2),
                                 "do_tin_cay": round(min(1.0, s["total"] / FULL_CONF), 2),
                                 "nguon": "bai_kiem_tra", "cap_nhat": now})
            if ratio >= STRONG:
                nl["diem_manh"].append(cid)
            elif ratio < WEAK:
                nl["diem_yeu"].append(cid)
        nl["da_test_dau_vao"] = True
    return sm


def grade_node(state: PlanState) -> dict:
    print(">>> [TEST] entry_grade")
    et = state["entry_test"]
    last = next((str(m.content) for m in reversed(state.get("messages", [])) if isinstance(m, HumanMessage)), "")
    ans = parse_answers(last)
    if not ans:
        return {"roadmap_status": "awaiting_test_answers", "messages": [AIMessage(
            content="Mình chưa đọc được đáp án. Bạn gửi theo dạng 1-a, 2-b, 3-c, ... giúp mình nhé.")]}

    key = json.loads(Path(et["key_file"]).read_text(encoding="utf-8"))["questions"]
    res = grade(key, ans)
    sm = update_profile(json.loads(json.dumps(state["student_model"])), et["subject"], res)
    lines = [f"Chương {c}: {s['correct']}/{s['total']}" for c, s in res["chapters"].items()]
    text = f"Bạn đúng {res['correct']}/{res['total']} câu. " + "; ".join(lines) + "."
    if res["answered"] < res["total"]:
        text += f" ({res['total'] - res['answered']} câu chưa trả lời, tính là sai.)"
    inbox = list(state.get("inbox", [])) + [{"sender": "roadmap", "receiver": "progress", "type": "update_profile",
                                             "payload": {"answers": normalize_answers(ans), "result": res}}]
    return {"student_model": sm, "entry_test": {**et, "result": res}, "inbox": inbox,
            "messages": [AIMessage(content=text)], "roadmap_status": "test_graded"}