"""Read-only roadmap display API.
Set EDU_UI_ROADMAPS_JSON to a JSON export produced by the Planning Agent.
No sample plans are generated and no fake progress is returned.
Format: {"roadmaps":[{"id":"...","subject":"Toán 10","title":"...",
"phases":[{"title":"...","description":"...","objectives":["..."],
"sessions":[{"title":"...","duration_minutes":45,"status":"pending"}]}]}]}
"""
import json
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
router = APIRouter(prefix="/api/ui/roadmaps", tags=["roadmap"])
@router.get("")
def list_roadmaps():
    source = os.getenv("EDU_UI_ROADMAPS_JSON", "").strip()
    if not source:
        return {"roadmaps": [], "connected": False}
    path = Path(source)
    if not path.is_file():
        raise HTTPException(status_code=503, detail="Chưa tìm thấy file dữ liệu lộ trình")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=503, detail="Không đọc được dữ liệu lộ trình") from exc
    if not isinstance(data, dict) or not isinstance(data.get("roadmaps"), list):
        raise HTTPException(status_code=503, detail="Dữ liệu lộ trình phải có trường roadmaps là danh sách")
    return {"roadmaps": data["roadmaps"], "connected": True}
