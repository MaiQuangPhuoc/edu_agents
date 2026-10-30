"""Local EDUAGENT UI workflow jobs. Run one uvicorn worker (in-memory sessions)."""
import asyncio
import logging
import os
import re
import time
import uuid
from typing import Literal
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .workflow_engine import engine
from .workflow_view import project, public_questions, answer_text

router = APIRouter(prefix="/api/ui/workflows", tags=["workflows"])
logger = logging.getLogger(__name__)
SESSIONS = {}
JOBS = {}
TASKS = set()
LABELS = {
    "queued": "Đang chờ lượt xử lý", "initializing": "Đang chuẩn bị AI và kho tài liệu",
    "router": "Đang xác định yêu cầu", "guard": "Đang xác định yêu cầu",
    "knowledge": "Đang tra cứu kiến thức", "solve": "Đang giải bài tập",
    "response": "Đang tổng hợp câu trả lời", "clarify": "Đang làm rõ câu hỏi",
    "tool": "Đang sử dụng công cụ", "collect_info": "Đang thu thập yêu cầu đề",
    "collect": "Đang cập nhật hồ sơ học tập", "retrieve_docs": "Đang tìm tài liệu",
    "build_knowledge": "Đang phân tích chủ đề", "build_matrix": "Đang xây dựng ma trận đề",
    "build_specs": "Đang thiết kế câu hỏi", "generate_questions": "Đang sinh đề kiểm tra",
    "evaluate_exam": "Đang kiểm tra chất lượng đề", "entry_test": "Đang chuẩn bị bài đầu vào",
    "entry_grade": "Đang chấm bài đầu vào", "planning": "Đang xây dựng sườn lộ trình",
    "learning_path": "Đang xây dựng lộ trình chi tiết", "outline": "Đang phân bổ các tuần",
    "plan": "Đang lập nhiệm vụ", "execute": "Đang tìm kiến thức và tài nguyên",
    "assemble": "Đang soạn từng buổi học", "critic": "Đang rà soát lộ trình",
    "present": "Đang lưu lộ trình", "practice": "Đang tạo và kiểm tra bài ôn tập",
}


class Create(BaseModel):
    mode: Literal["qa", "exam", "planning"] = "qa"


class Turn(BaseModel):
    message: str = Field(min_length=1, max_length=15000)
    request_id: str = Field(min_length=1, max_length=80)
    revision: int = Field(ge=0)
    lp_verify: bool = False


class Entry(BaseModel):
    answers: dict[str, str]
    request_id: str = Field(min_length=1, max_length=80)
    revision: int = Field(ge=0)


class Practice(BaseModel):
    week_no: int
    session_no: int = Field(ge=1)
    request_id: str = Field(min_length=1, max_length=80)
    revision: int = Field(ge=0)


def get_session(sid):
    if sid not in SESSIONS:
        raise HTTPException(410, "Phiên đã hết hạn hoặc server vừa khởi động lại. Hãy tạo cuộc trò chuyện mới.")
    return SESSIONS[sid]


def view(session):
    if session["mode"] == "exam":
        from src.edu_exam.curriculum import get_chapter
        return project(session, get_chapter)
    return project(session)


def export_exam(session, questions):
    """Publish the exact finished questions under a catalog-compatible filename."""
    from .exam_api import SOURCE_DIR, save
    subject = session["state"].get("student_profile", {}).get("mon_hoc") or (session["state"].get("lp_window") or {}).get("subject")
    slug = {"Toán 10": "toan", "Ngữ văn 10": "ngu_van", "Lịch sử 10": "lich_su"}.get(subject)
    if not slug or not questions:
        raise ValueError("Chưa có môn học hoặc câu hỏi hợp lệ để mở đề.")
    if any(not isinstance(q, dict) or not q.get("question") or not isinstance(q.get("options"), dict)
           or str(q.get("answer", "")) not in q["options"] for q in questions):
        raise ValueError("Đề chưa có đầy đủ câu hỏi và đáp án hợp lệ.")
    stem = f"{slug}_ui_{uuid.uuid4().hex}"
    save(SOURCE_DIR / f"{stem}.json", {"title": f"Bài kiểm tra {subject}", "questions": questions})
    return "/exams?" + urlencode({"exam": "test_exam--" + stem, "view": "take", "student_id": session["student_id"]})


def add_progress(job, name):
    if name not in LABELS:
        return
    if not job["steps"] or job["steps"][-1]["code"] != name:
        job["steps"].append({"code": name, "label": LABELS[name]})
    job["steps"] = job["steps"][-50:]


async def work(session, job, text=None, lesson=None):
    try:
        # Existing generators write shared caches/files; serialize jobs for this local app.
        async with engine.lock:
            job["status"] = "running"
            if lesson is not None:
                await engine.graph("exam")
                add_progress(job, "practice")
                result = await asyncio.to_thread(engine.practice, session, lesson)
                url = export_exam(session, result["exam"])
                job["result"] = {"exam_url": url, "tests": result.get("tests", [])}
            else:
                await engine.run(session, text, lambda name: add_progress(job, name))
                if session["mode"] == "exam" and session["state"].get("evaluate_done"):
                    session["exam_url"] = export_exam(session, session["state"].get("final_exam") or session["state"].get("generated_exam"))
                session["revision"] += 1
                job["result"] = view(session)
            job["status"] = "completed"
    except asyncio.CancelledError:
        job.update(status="failed", error="Server đã dừng tác vụ. Kiểm tra kết quả đã lưu trước khi chạy lại.")
        raise
    except Exception:
        logger.exception("Workflow failed: job=%s mode=%s", job["id"], session["mode"])
        # Do not expose provider credentials, prompts or stack traces to the browser.
        job.update(status="failed", error="Không hoàn tất được tác vụ. Xem log server theo mã tác vụ, rồi thử lại.")
    finally:
        session["busy"] = False


def start(session, request_id, revision, *, text=None, lesson=None):
    previous = session["requests"].get(request_id)
    if previous:
        return {"job_id": previous, "session_id": session["id"]}
    if session["busy"]:
        raise HTTPException(409, "Phiên này đang xử lý. Vui lòng chờ kết quả hiện tại.")
    if revision != session["revision"]:
        raise HTTPException(409, "Thao tác thuộc phiên bản cũ. Tải lại cuộc trò chuyện trước khi xác nhận.")
    if len(JOBS) >= 1000:
        expired = [key for key, job in JOBS.items() if job["status"] in ("completed", "failed") and time.time() - job["created"] > 86400]
        for key in expired:
            JOBS.pop(key)
        if len(JOBS) >= 1000:
            raise HTTPException(503, "Bộ nhớ tác vụ đã đầy; hãy khởi động lại UI khi các tác vụ đang chạy hoàn tất.")
    jid = uuid.uuid4().hex
    job = {"id": jid, "session_id": session["id"], "status": "queued", "steps": [], "created": time.time()}
    add_progress(job, "queued")
    JOBS[jid] = job
    session["requests"][request_id] = jid
    session.update(busy=True, last_job=jid)
    task = asyncio.create_task(work(session, job, text, lesson))
    TASKS.add(task)
    task.add_done_callback(TASKS.discard)
    return {"job_id": jid, "session_id": session["id"]}


@router.post("")
def create(body: Create):
    if len(SESSIONS) >= 200:
        raise HTTPException(503, "Đã đạt giới hạn phiên của tiến trình UI. Khởi động lại khi các tác vụ hoàn tất.")
    sid = uuid.uuid4().hex
    student_id = os.getenv("EDU_UI_STUDENT_ID", "hs_002")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", student_id):
        raise HTTPException(500, "EDU_UI_STUDENT_ID không hợp lệ.")
    SESSIONS[sid] = {"id": sid, "student_id": student_id, "mode": body.mode, "state": {},
                     "revision": 0, "busy": False, "requests": {}, "lp_verify": False}
    return {"session_id": sid, "mode": body.mode, "revision": 0, "student_id": student_id}


@router.get("/jobs/{jid}")
def job_status(jid: str):
    if jid not in JOBS:
        raise HTTPException(410, "Tác vụ không còn trong bộ nhớ. Server có thể đã khởi động lại.")
    return JOBS[jid]


@router.get("/identity")
def identity():
    return {"student_id": os.getenv("EDU_UI_STUDENT_ID", "hs_002")}


@router.post("/saved")
def saved_path():
    from src.edu_planning.path_store import load_learning_path
    from src.edu_planning.student_store import load_student_model
    created = create(Create(mode="planning"))
    session = get_session(created["session_id"])
    lp = load_learning_path(session["student_id"])
    if not lp:
        SESSIONS.pop(session["id"])
        raise HTTPException(404, "Chưa có lộ trình đã lưu cho học sinh hiện tại.")
    # Older files may lack subject: leave blank instead of guessing the first subject.
    session["state"] = {"learning_path": lp, "lp_window": {"subject": lp.get("subject", "")},
                        "student_model": load_student_model(session["student_id"]) or {},
                        "roadmap_status": "path_ready", "messages": []}
    return created


@router.get("/{sid}")
def snapshot(sid: str):
    session = get_session(sid)
    return {**view(session), "busy": session["busy"], "last_job": session.get("last_job"),
            "student_id": session["student_id"], "lp_verify": session["lp_verify"]}


@router.post("/{sid}/messages")
async def message(sid: str, body: Turn):
    session = get_session(sid)
    if body.request_id in session["requests"]:
        return start(session, body.request_id, body.revision)
    if not body.message.strip():
        raise HTTPException(422, "Tin nhắn không được để trống.")
    if not session["busy"]:
        session["lp_verify"] = body.lp_verify
    if session["mode"] == "planning" and session["state"].get("roadmap_status") == "path_ready":
        raise HTTPException(409, "Lộ trình đã hoàn tất. Mở lộ trình hoặc tạo cuộc trò chuyện mới để lập lộ trình khác.")
    if session["mode"] == "exam" and session["state"].get("evaluate_done"):
        raise HTTPException(409, "Đề đã hoàn tất. Mở đề hoặc tạo cuộc trò chuyện mới để tạo đề khác.")
    return start(session, body.request_id, body.revision, text=body.message)


@router.get("/{sid}/entry-test")
def entry_test(sid: str):
    session = get_session(sid)
    if session["state"].get("roadmap_status") != "awaiting_test_answers":
        raise HTTPException(409, "Phiên không chờ làm bài kiểm tra đầu vào.")
    entry = session["state"].get("entry_test") or {}
    questions = public_questions(entry.get("questions", []))
    if not questions:
        raise HTTPException(422, "Bài test thiếu dữ liệu UI. Kiểm tra bản cập nhật entry_test.py.")
    return {"subject": entry.get("subject"), "questions": questions, "revision": session["revision"]}


@router.post("/{sid}/entry-test")
async def submit_entry(sid: str, body: Entry):
    session = get_session(sid)
    if body.request_id in session["requests"]:
        return start(session, body.request_id, body.revision)
    questions = entry_test(sid)["questions"]
    try:
        text = answer_text(questions, body.answers)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return start(session, body.request_id, body.revision, text=text)


@router.get("/{sid}/path")
def path_data(sid: str):
    session = get_session(sid)
    lp = session["state"].get("learning_path")
    if not lp:
        raise HTTPException(404, "Lộ trình chi tiết chưa sẵn sàng.")
    return {"path": lp, "subject": (session["state"].get("lp_window") or {}).get("subject", ""),
            "student_id": session["student_id"], "revision": session["revision"]}


@router.post("/{sid}/practice")
async def practice(sid: str, body: Practice):
    session = get_session(sid)
    if body.request_id in session["requests"]:
        return start(session, body.request_id, body.revision)
    lp = path_data(sid)["path"]
    week = next((w for w in lp.get("weeks", []) if w["week_no"] == body.week_no), None)
    if not week or body.session_no > len(week.get("sessions", [])):
        raise HTTPException(404, "Không tìm thấy buổi học.")
    lesson = week["sessions"][body.session_no - 1]
    if not lesson.get("exam_enabled", False):
        raise HTTPException(403, "Buổi này chưa bật tạo bài kiểm tra.")
    return start(session, body.request_id, body.revision, lesson=lesson)
