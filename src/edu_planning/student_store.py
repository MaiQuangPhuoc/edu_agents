import json
import os
import re
from pathlib import Path
from typing import Optional

STUDENT_DIR = Path(
    os.getenv(
        "EDU_STUDENT_STORE_DIR",
        str(Path(__file__).resolve().parents[2] / "store" / "student"),
    )
)


def _student_path(student_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", student_id):
        raise ValueError("student_id không hợp lệ")
    return STUDENT_DIR / f"{student_id}.json"


def save_student_model(model: dict) -> Path:
    path = _student_path(model["student_id"])
    STUDENT_DIR.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(model, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(path)
    return path


def load_student_model(student_id: str) -> Optional[dict]:
    path = _student_path(student_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))