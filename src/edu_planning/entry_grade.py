"""Chấm bài trắc nghiệm và cập nhật năng lực theo chương."""
import re, json, copy
from datetime import datetime
from pathlib import Path
from langchain_core.messages import AIMessage, HumanMessage
from src.edu_planning.student_store import save_student_model
from src.edu_planning.collect_student_model import _make_queries

def parse_answers(text: str) -> dict[int, str]:
    """'1-A, 2 - C, 3.b' -> {1: 'A', 2: 'C', 3: 'B'}."""
    return {int(n): a.upper() for n, a in re.findall(r"\b(\d+)\s*[-.:)]?\s*([A-Da-d])\b", text)}


def grade(questions: list[dict], answers: dict[int, str]) -> dict:
    chapters = {}
    for q in questions:
        cid = q["chapter_id"]
        ch = chapters.setdefault(cid, {"correct": 0, "total": 0})
        ch["total"] += 1
        ch["correct"] += answers.get(q["no"]) == q["answer"].upper()
    for ch in chapters.values():
        ch["ratio"] = round(ch["correct"] / ch["total"], 2)
        ch["level"] = "Mạnh" if ch["ratio"] >= 0.7 else "Yếu" if ch["ratio"] < 0.5 else "Trung bình"
    return {"correct": sum(c["correct"] for c in chapters.values()),
            "total": len(questions), "chapters": chapters}


def update_profile(student_model: dict, subject: str, result: dict) -> dict:
    """Cập nhật hồ sơ theo kết quả bài test (thay số liệu cũ của những chương đã test)."""
    now = datetime.now().isoformat()
    for nl in student_model.get("nang_luc", []):
        if nl.get("mon_hoc") != subject:
            continue
        tested = result["chapters"]
        nl["chu_de"] = [x for x in nl.get("chu_de", []) if x.get("chapter_id") not in tested]
        nl["diem_manh"] = [x for x in nl.get("diem_manh", []) if x not in tested]
        nl["diem_yeu"] = [x for x in nl.get("diem_yeu", []) if x not in tested]
        for cid, info in tested.items():
            nl["chu_de"].append({"chapter_id": cid, "lesson": "", "muc_nam": info["ratio"],
                                 "do_tin_cay": round(min(info["total"] / 5, 1), 2),
                                 "nguon": "bai_kiem_tra", "cap_nhat": now})
            if info["level"] == "Mạnh":
                nl["diem_manh"].append(cid)
            elif info["level"] == "Yếu":
                nl["diem_yeu"].append(cid)
        nl["da_test_dau_vao"] = True
    student_model["updated_at"] = now
    return student_model

def entry_grade_node(state, llm_client) -> dict:
    print(">>> [TEST] entry_grade")
    et = state["entry_test"]
    last = next((str(m.content) for m in reversed(state.get("messages", [])) if isinstance(m, HumanMessage)), "")
    answers = parse_answers(last)
    key = json.loads(Path(et["key_file"]).read_text(encoding="utf-8"))["questions"]
    missing = sorted({q["no"] for q in key} - set(answers))
    if missing:                                   # thiếu câu: hỏi lại toàn bộ
        return {"roadmap_status": "awaiting_test_answers", "messages": [AIMessage(
            content=f"Cần đủ {len(key)} câu, còn thiếu: {missing}. Bạn gửi lại toàn bộ đáp án theo dạng 1-a, 2-b, ... nhé.")]}

    result = grade(key, answers)
    model = update_profile(copy.deepcopy(state["student_model"]), et["subject"], result)
    save_student_model(model)
    lines = [f"Chương {c}: {i['correct']}/{i['total']} - {i['level']}" for c, i in sorted(result["chapters"].items())]
    text = f"Kết quả: {result['correct']}/{result['total']} câu đúng.\n" + "\n".join(lines)
    return {"student_model": model, "entry_test": {**et, "result": result}, "entry_done": True,
            "search_queries": _make_queries(model, state, llm_client),     # tạo lại query theo hồ sơ sau test
            "roadmap_status": "", "messages": [AIMessage(content=text)]}