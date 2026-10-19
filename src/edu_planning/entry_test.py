"""Bài test đầu vào giả lập: chọn câu -> cho học sinh làm -> chấm -> cập nhật hồ sơ."""
import copy
import json
import random
from pathlib import Path

from src.edu_planning.entry_grade import parse_answers, grade, update_profile
from src.edu_planning.student_store import save_student_model

BANK_FILE = Path(__file__).resolve().parents[1] / "entry_test_demo" / "question_bank_toan10.json"


def make_test(student_model: dict, total: int = 20) -> list[dict]:
    bank = json.loads(BANK_FILE.read_text(encoding="utf-8"))
    subject = bank["subject"]
    skills = next((x for x in student_model.get("nang_luc", []) if x["mon_hoc"] == subject), {})
    weak = set(skills.get("diem_yeu", []))
    strong = set(skills.get("diem_manh", []))
    # Chỉ test các chương học sinh đã đề cập; nếu chưa có thì dùng mọi chương trong bank.
    chapters = weak | strong or {q["chapter_id"] for q in bank["questions"]}
    # Mỗi chương lấy ít nhất 3 câu (nếu đủ), phần còn lại ưu tiên chương yếu.
    pools = {c: random.sample([q for q in bank["questions"] if q["chapter_id"] == c],
                              k=len([q for q in bank["questions"] if q["chapter_id"] == c])) for c in chapters}
    pools = {c: qs for c, qs in pools.items() if qs}
    chosen = []
    for c in sorted(pools):
        for _ in range(min(3, len(pools[c]))):
            if len(chosen) < total:
                chosen.append(pools[c].pop())
    while len(chosen) < total and any(pools.values()):
        available = [c for c in pools if pools[c]]
        weights = [3 if c in weak else 1 for c in available]
        c = random.choices(available, weights=weights, k=1)[0]
        chosen.append(pools[c].pop())
    random.shuffle(chosen)
    return [{"no": i, **q} for i, q in enumerate(chosen, 1)]


def show_test(questions: list[dict]) -> None:
    print(f"\n=== BÀI KIỂM TRA ĐẦU VÀO ({len(questions)} câu) ===")
    for q in questions:
        print(f"\nCâu {q['no']} (Chương {q['chapter_id']}): {q['question']}")
        for letter, value in q["options"].items():
            print(f"  {letter}. {value}")
    print("\nNhập đáp án theo mẫu: 1-A, 2-C, 3-B, ...")


def run_entry_test(student_model: dict) -> tuple[dict, dict]:
    questions = make_test(student_model)
    if not questions:
        raise ValueError("Ngân hàng không có câu hỏi phù hợp")
    show_test(questions)
    expected = {q["no"] for q in questions}
    while True:
        answers = parse_answers(input("\nĐáp án của bạn: "))
        if set(answers) == expected:
            break
        print(f"Cần đủ {len(questions)} câu, còn thiếu: {sorted(expected - set(answers))}. Hãy nhập lại toàn bộ đáp án.")

    result = grade(questions, answers)
    print(f"\nKẾT QUẢ: {result['correct']}/{result['total']} câu đúng")
    for cid, info in sorted(result["chapters"].items()):
        print(f"Chương {cid}: {info['correct']}/{info['total']} — {info['level']} ({info['ratio']*100:.0f}%)")

    updated = update_profile(copy.deepcopy(student_model), "Toán 10", result)
    save_student_model(updated)
    print("Đã cập nhật và lưu StudentModel.")
    return updated, result
