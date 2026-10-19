"""Chấm bài trắc nghiệm và cập nhật năng lực theo chương."""
import re
from datetime import datetime


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
