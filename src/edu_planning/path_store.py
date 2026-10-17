import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from typing import Optional
from src.edu_planning.student_store import STUDENT_DIR
from src.edu_planning.path_format import to_markdown

PATH_DIR = STUDENT_DIR.parent / "learning_path"       # đổi theo cấu trúc dự án


def save_learning_path(student_id: str, lp: dict) -> Path:
    """Lưu JSON (nguồn chính) và bản Markdown (tạo từ JSON) cạnh nhau. Trả về đường dẫn file JSON."""
    PATH_DIR.mkdir(parents=True, exist_ok=True)
    path = PATH_DIR / f"{student_id}.json"
    path.write_text(json.dumps(lp, ensure_ascii=False, indent=2), encoding="utf-8")
    path.with_suffix(".md").write_text(to_markdown(lp), encoding="utf-8")
    return path


def load_learning_path(student_id: str) -> Optional[dict]:
    path = PATH_DIR / f"{student_id}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None