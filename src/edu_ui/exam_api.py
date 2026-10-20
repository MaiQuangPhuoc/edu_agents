"""Read-only exam catalog + persisted attempts for EDUAGENT UI.
Place actual curated/generated exams in data/edu_ui_exams/catalog.json.
Never expose correct answers in uncompleted exam responses.
Demo student_id query argument must be replaced by authenticated identity in production.
"""
import json
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/ui/exams", tags=["ui-exams"])
DATA = Path(__file__).resolve().parents[2] / "data" / "edu_ui_exams"
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

def catalog():
    exams = read_json(DATA / "catalog.json", [])
    if not isinstance(exams, list):
        raise HTTPException(500, "catalog.json phải là danh sách đề")
    return exams

def find_exam(exam_id):
    match = next((e for e in catalog() if e.get("exam_id") == exam_id), None)
    if not match:
        raise HTTPException(404, "Không tìm thấy đề kiểm tra")
    return match

def questions_public(exam):
    return [{"id": str(q["id"]), "text": q["text"], "options": q["options"]} for q in exam.get("questions", [])]

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)

@router.get("")
def list_exams(student_id: str):
    attempts = read_json(student_file(student_id), {})
    out = []
    for exam in catalog():
        eid = exam["exam_id"]
        attempt = attempts.get(eid)
        out.append({"exam_id": eid, "title": exam.get("title", eid),
                    "subject": exam.get("subject", "Khác"),
                    "created_at": exam.get("created_at"),
                    "last_activity": attempt.get("submitted_at") if attempt else exam.get("created_at"),
                    "question_count": len(exam.get("questions", [])), "completed": bool(attempt)})
    return {"exams": out}

@router.get("/{exam_id}")
def get_exam(exam_id: str, student_id: str):
    exam = find_exam(exam_id)
    attempt = read_json(student_file(student_id), {}).get(exam_id)
    data = {"exam_id": exam_id, "title": exam.get("title", exam_id),
            "subject": exam.get("subject", "Khác"),
            "questions": questions_public(exam), "completed": bool(attempt)}
    if attempt:
        data["result"] = attempt
    return data

@router.post("/{exam_id}/submit")
def submit(exam_id: str, student_id: str, body: Answers):
    exam = find_exam(exam_id)
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
        attempts = read_json(path, {})
        if exam_id in attempts:
            raise HTTPException(409, "Bài này đã được nộp")
        attempts[exam_id] = result
        save(path, attempts)
    return {"result": result}
