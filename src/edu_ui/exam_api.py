"""Exam catalog and persisted attempts for EDUAGENT UI.
A configured data/edu_ui_exams/catalog.json takes precedence; otherwise valid
question sets are discovered in src/test_exam and src/test_exam copy.
Files without questions, options, and answer keys are not treated as exams.
Correct answers are hidden until an attempt is submitted.
Demo student_id query argument must be replaced by authenticated identity in production.
"""
import json
import hashlib
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/ui/exams", tags=["ui-exams"])
DATA = Path(__file__).resolve().parents[2] / "data" / "edu_ui_exams"
SOURCE_DIRS = (
    (Path(__file__).resolve().parents[1] / "test_exam", "test_exam"),
    (Path(__file__).resolve().parents[1] / "test_exam copy", "test_exam-copy"),
)
DEMO_FILE = Path(__file__).resolve().parent / "demo_data" / "exams.json"
LOCK = threading.RLock()

class Answers(BaseModel):
    answers: dict[str, str] = Field(default_factory=dict)

def student_file(student_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", student_id):
        raise HTTPException(422, "student_id không hợp lệ")
    return DATA / "attempts" / f"{student_id}.json"

def read_json(path: Path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise HTTPException(500, f"Không đọc được dữ liệu: {path.name}") from exc

def source_exams():
    exams = []
    seen_fingerprints = set()
    for directory, source_name in SOURCE_DIRS:
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("exam_*.json")):
            try:
                raw = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, ValueError) as exc:
                raise HTTPException(
                    500, f"Không đọc được đề kiểm tra: {path.name}"
                ) from exc

            questions = raw.get("questions") if isinstance(raw, dict) else raw
            if not isinstance(questions, list) or not questions:
                continue
            if any(
                not isinstance(question, dict)
                or not isinstance(question.get("question"), str)
                or not question["question"].strip()
                or not isinstance(question.get("options"), dict)
                or len(question["options"]) < 2
                or str(question.get("answer", "")) not in question["options"]
                for question in questions
            ):
                continue

            fingerprint_data = [
                {
                    "question": question["question"].strip(),
                    "options": question["options"],
                    "answer": str(question["answer"]),
                }
                for question in questions
            ]
            fingerprint = hashlib.sha256(
                json.dumps(
                    fingerprint_data, ensure_ascii=False, sort_keys=True
                ).encode("utf-8")
            ).hexdigest()
            if fingerprint in seen_fingerprints:
                continue
            seen_fingerprints.add(fingerprint)

            chapters = list(dict.fromkeys(
                str(question.get("chuong", "")).strip()
                for question in questions
                if question.get("chuong")
            ))
            topics = list(dict.fromkeys(
                str(question.get("bai", "")).strip()
                for question in questions
                if question.get("bai")
            ))
            chapter_summary = " · ".join(chapters[:3])
            exam_date = None
            try:
                exam_date = datetime.strptime(
                    path.stem.removeprefix("exam_"), "%Y%m%d_%H%M%S"
                ).replace(tzinfo=timezone.utc).isoformat()
            except ValueError:
                pass

            exams.append({
                "exam_id": f"{source_name}--{path.stem}",
                "title": f"Đề luyện tập {len(exams) + 1:02d}",
                "subject": "Toán 10",
                "chapter": chapter_summary or "Ôn tập tổng hợp",
                "topics": topics,
                "source_file": f"{source_name}/{path.name}",
                "created_at": exam_date,
                "questions": [
                    {
                        "id": f"q{index}",
                        "text": question["question"].strip(),
                        "options": question["options"],
                        "answer": str(question["answer"]),
                        "explanation": question.get("giai_thich", ""),
                    }
                    for index, question in enumerate(questions, start=1)
                ],
            })
    return exams


def catalog():
    exams = read_json(DATA / "catalog.json", None)
    if exams is None:
        exams = source_exams()
    if not isinstance(exams, list):
        raise HTTPException(500, "catalog.json phải là danh sách đề")
    if exams:
        return exams, False
    return read_json(DEMO_FILE, []), True

def load_attempts(student_id: str, demo: bool):
    path = student_file(student_id)
    if path.is_file():
        return read_json(path, {})
    if student_id == "hs_002" and demo:
        example = Path(__file__).resolve().parent / "demo_data" / "attempts.json"
        return read_json(example, {})
    return {}

def find_exam(exam_id):
    exams, demo = catalog()
    match = next((e for e in exams if e.get("exam_id") == exam_id), None)
    if not match:
        raise HTTPException(404, "Không tìm thấy đề kiểm tra")
    return match, demo

def questions_public(exam, include_explanations=False):
    questions = []
    for question in exam.get("questions", []):
        public = {
            "id": str(question["id"]),
            "text": question["text"],
            "options": question["options"],
        }
        if include_explanations and question.get("explanation"):
            public["explanation"] = question["explanation"]
        questions.append(public)
    return questions

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)

@router.get("")
def list_exams(student_id: str):
    exams, demo = catalog()
    attempts = load_attempts(student_id, demo)
    out = []
    for exam in exams:
        eid = exam["exam_id"]
        attempt = attempts.get(eid)
        out.append({"exam_id": eid, "title": exam.get("title", eid),
                    "subject": exam.get("subject", "Khác"),
                    "chapter": exam.get("chapter", ""),
                    "topics": exam.get("topics", []),
                    "created_at": exam.get("created_at"),
                    "last_activity": attempt.get("submitted_at") if attempt else exam.get("created_at"),
                    "question_count": len(exam.get("questions", [])), "completed": bool(attempt)})
    return {"exams": out, "demo": demo}

@router.get("/{exam_id}")
def get_exam(exam_id: str, student_id: str):
    exam, demo = find_exam(exam_id)
    attempt = load_attempts(student_id, demo).get(exam_id)
    data = {"exam_id": exam_id, "title": exam.get("title", exam_id),
            "subject": exam.get("subject", "Khác"),
            "chapter": exam.get("chapter", ""),
            "topics": exam.get("topics", []),
            "questions": questions_public(exam, include_explanations=bool(attempt)),
            "completed": bool(attempt)}
    if attempt:
        data["result"] = attempt
    return data

@router.post("/{exam_id}/submit")
def submit(exam_id: str, student_id: str, body: Answers):
    exam, demo = find_exam(exam_id)
    path = student_file(student_id)
    questions = exam.get("questions", [])
    if not questions:
        raise HTTPException(422, "Đề kiểm tra chưa có câu hỏi")
    allowed_ids = {str(q["id"]) for q in questions}
    if not set(body.answers).issubset(allowed_ids):
        raise HTTPException(422, "Có câu trả lời không thuộc đề")
    for q in questions:
        answer = body.answers.get(str(q["id"]))
        if answer is not None and answer not in q["options"]:
            raise HTTPException(422, "Đáp án không hợp lệ")
    correct_answers = {str(q["id"]): str(q["answer"]) for q in questions}
    correct = sum(body.answers.get(qid) == ans for qid, ans in correct_answers.items())
    result = {"answers": body.answers, "correct_answers": correct_answers,
              "correct": correct, "total": len(questions),
              "percent": round(correct * 100 / len(questions), 1),
              "submitted_at": datetime.now(timezone.utc).isoformat()}
    with LOCK:
        attempts = load_attempts(student_id, demo)
        if exam_id in attempts:
            raise HTTPException(409, "Bài này đã được nộp")
        attempts[exam_id] = result
        save(path, attempts)
    return {"result": result}
