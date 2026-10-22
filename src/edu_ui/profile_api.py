"""Read and save student profiles using the canonical planning StudentModel."""
import json
import re
import threading
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException

from src.edu_planning.student_store import STUDENT_DIR
from src.state_plan import StudentModel

router = APIRouter(prefix="/api/ui/students", tags=["student-profile"])
DATA = STUDENT_DIR
LOCK = threading.RLock()


def storage(student_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", student_id):
        raise HTTPException(status_code=422, detail="student_id không hợp lệ")
    return DATA / f"{student_id}.json"


def read_profile(path: Path, student_id: str) -> StudentModel:
    if not path.exists():
        return StudentModel(student_id=student_id)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return StudentModel.model_validate(data)
    except (OSError, ValueError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Không thể đọc hồ sơ học sinh {path.stem}",
        ) from exc


def write_profile(path: Path, profile: StudentModel) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(profile.model_dump(mode="json"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(path)


@router.get("/{student_id}/profile")
def get_profile(student_id: str) -> StudentModel:
    path = storage(student_id)
    with LOCK:
        return read_profile(path, student_id)


@router.put("/{student_id}/profile")
def save_profile(student_id: str, profile: StudentModel) -> StudentModel:
    if profile.student_id != student_id:
        raise HTTPException(
            status_code=422,
            detail="student_id trong hồ sơ không khớp với đường dẫn",
        )
    path = storage(student_id)
    with LOCK:
        previous = read_profile(path, student_id)
        updated = profile.model_copy(
            update={
                "version": previous.version + 1,
                "updated_at": datetime.now(timezone.utc),
            }
        )
        try:
            write_profile(path, updated)
        except OSError as exc:
            raise HTTPException(
                status_code=500,
                detail="Không thể lưu hồ sơ học sinh",
            ) from exc
    return updated
