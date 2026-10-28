"""Grade-10 exam library from src/test_exam only.
Subject is determined by the filename prefix, never inferred by an LLM.
Answer keys remain server-side until submission.
"""
import json
import logging
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/ui/exams", tags=["ui-exams"])
DATA = Path(__file__).resolve().parents[2] / "data" / "edu_ui_exams"
SOURCE_DIR = Path(__file__).resolve().parents[1] / "test_exam"
SUBJECT_PREFIXES = {
    "toan": "Toán 10", "ngu_van": "Ngữ văn 10", "van": "Ngữ văn 10",
    "lich_su": "Lịch sử 10", "tieng_anh": "Tiếng Anh 10", "anh": "Tiếng Anh 10",
    "vat_li": "Vật lí 10", "vat_ly": "Vật lí 10", "hoa_hoc": "Hóa học 10",
    "sinh_hoc": "Sinh học 10", "dia_li": "Địa lí 10", "dia_ly": "Địa lí 10",
    "tin_hoc": "Tin học 10", "cong_nghe": "Công nghệ 10",
    "gdktpl": "Giáo dục kinh tế và pháp luật 10", "gdqp": "Giáo dục quốc phòng và an ninh 10",
    "gd_the_chat": "Giáo dục thể chất 10", "am_nhac": "Âm nhạc 10", "mi_thuat": "Mĩ thuật 10",
}
logger = logging.getLogger(__name__)


def subject_from_filename(filename):
    stem = Path(filename).stem.casefold()
    for prefix in sorted(SUBJECT_PREFIXES, key=len, reverse=True):
        if stem.startswith(prefix + "_"):
            return SUBJECT_PREFIXES[prefix]
    return None


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
    if not SOURCE_DIR.is_dir():
        return exams
    for path in sorted(SOURCE_DIR.glob("*.json")):
        subject = subject_from_filename(path.name)
        if not subject:
            logger.warning("Bỏ qua %s: chưa có tiền tố môn học hợp lệ.", path.name)
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as exc:
            raise HTTPException(500, f"Không đọc được đề kiểm tra: {path.name}") from exc
        questions = raw.get("questions") if isinstance(raw, dict) else raw
        if not isinstance(questions, list) or not questions or any(
            not isinstance(q, dict) or not isinstance(q.get("question"), str)
            or not q["question"].strip() or not isinstance(q.get("options"), dict)
            or len(q["options"]) < 2 or str(q.get("answer", "")) not in q["options"]
            or any(not isinstance(value, str) for value in q["options"].values())
            for q in questions
        ):
            logger.warning("Bỏ qua %s: thiếu câu hỏi, lựa chọn hoặc đáp án hợp lệ.", path.name)
            continue
        chapters = list(dict.fromkeys(str(q["chuong"]).strip() for q in questions if q.get("chuong")))
        topics = list(dict.fromkeys(str(q["bai"]).strip() for q in questions if q.get("bai")))
        created_at = None
        date = re.search(r"(\d{8}_\d{6})$", path.stem)
        if date:
            try:
                created_at = datetime.strptime(date[1], "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc).isoformat()
            except ValueError:
                pass
        default_title = path.stem.replace("_", " ")
        title = raw.get("title") if isinstance(raw, dict) else None
        exams.append({
            "exam_id": f"test_exam--{path.stem}",
            "title": title.strip() if isinstance(title, str) and title.strip() else default_title,
            "subject": subject, "chapter": " · ".join(chapters[:3]) or "Ôn tập tổng hợp",
            "topics": topics, "source_file": f"test_exam/{path.name}", "created_at": created_at,
            "questions": [{"id": f"q{i}", "text": q["question"].strip(), "options": q["options"],
                           "answer": str(q["answer"]), "explanation": q.get("giai_thich", "")}
                          for i, q in enumerate(questions, 1)],
        })
    return exams


def catalog():
    # The user's chosen folder is the sole source; no demo or copy-folder fallback.
    return source_exams(), False


def load_attempts(student_id: str, demo: bool):
    path = student_file(student_id)
    if path.is_file():
        return read_json(path, {})
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

