import json
from pathlib import Path
from typing import Optional

STUDENT_DIR = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\store\student")   # đổi theo cấu trúc dự án


def save_student_model(model: dict) -> Path:
    STUDENT_DIR.mkdir(parents=True, exist_ok=True)
    path = STUDENT_DIR / f"{model['student_id']}.json"
    path.write_text(json.dumps(model, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_student_model(student_id: str) -> Optional[dict]:
    path = STUDENT_DIR / f"{student_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))