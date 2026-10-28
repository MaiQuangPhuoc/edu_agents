import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state_plan import PlanState
from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_planning.plan_search import wants_resources
from src.edu_planning.lp_tools import _build_schedule
from src.edu_planning.chapter_utils import normalize_chapter_id

MAX_WINDOW_CHAPTERS = 2      # số chương tối đa trong cửa sổ chi tiết (quy tắc tự đặt)


def phases_in_scope(state: PlanState) -> list[dict]:
    """Giai đoạn hiện tại và các giai đoạn sau, cùng môn."""
    phases = state.get("master_roadmap", {}).get("giai_doan", [])
    order = state.get("vi_tri_hien_tai") or 1
    cur = next((p for p in phases if p["thu_tu"] == order), phases[0] if phases else None)
    if not cur:
        return []
    return [p for p in phases if p["thu_tu"] >= cur["thu_tu"] and p.get("mon_hoc") == cur.get("mon_hoc")]


def build_window(state: PlanState) -> dict:
    """Cửa sổ chi tiết = TOÀN BỘ giai đoạn hiện tại (số tuần lấy từ outline)."""
    phase = phases_in_scope(state)[0]
    subject = phase["mon_hoc"]
    weeks = next(o["weeks"] for o in state["lp_outline"] if o["phase"] == phase["thu_tu"])
    lessons = {}
    for c in phase.get("chapters", []):
        cid = normalize_chapter_id(subject, c["chapter_id"]) or str(c["chapter_id"])
        lessons.setdefault(cid, []).extend(c["lessons"])
    return {
        "start_date": None, "num_weeks": len(weeks), "first_week_no": weeks[0]["week_no"],
        "phase": phase["thu_tu"], "phase_name": phase.get("ten", ""),
        "phase_goal": phase.get("muc_tieu", ""), "subject": subject,
        "chapter_ids": list(lessons), "chapter_lessons": lessons,
        "chapter_names": {c: get_subject_curriculum(subject).get(c, {}).get("chapter_name", "") for c in lessons},
    }


def window_text(w: dict) -> str:
    cur = get_subject_curriculum(w["subject"])
    lines = [f"Môn: {w['subject']} | Giai đoạn {w['phase']}: {w['phase_name']} | Mục tiêu: {w['phase_goal']}",
             f"Cửa sổ chi tiết: {w['num_weeks']} tuần. Các chương:"]
    for cid in w["chapter_ids"]:
        lines.append(f"- chapter_id={cid}: {cur.get(cid, {}).get('chapter_name', '')} | bài: {', '.join(w['chapter_lessons'][cid])}")
    return "\n".join(lines)


def student_text(sm: dict) -> str:
    keep = {k: v for k, v in sm.items() if k != "tien_do" and v not in (None, "", [], {})}
    return json.dumps(keep, ensure_ascii=False, separators=(",", ":"))

def make_tasks(w: dict, student_model: dict) -> list[dict]:
    """Việc cần làm sinh bằng code: mỗi chương một việc kiến thức (k_), và một việc tài nguyên (g_) nếu học sinh dùng video/tài liệu."""
    tasks = []
    for cid in w["chapter_ids"]:
        tasks.append({"id": f"k_{cid}", "kind": "knowledge", "chapter_id": cid, "depends_on": [],
                      "goal": f"Phân tích kiến thức từng bài của chương {cid}"})
        if wants_resources(student_model):
            tasks.append({"id": f"g_{cid}", "kind": "resources", "chapter_id": cid, "depends_on": [],
                          "goal": f"Tìm tài liệu và video cho chương {cid}"})
    return tasks


def plan_node(state: PlanState) -> dict:
    print(">>> ===============================  [LP] plan =============================== "*2)
    window = build_window(state)

    sched = _build_schedule(state["student_model"], window["subject"], window)
    if "error" in sched:
        return {"lp_draft": {"error": sched["error"]}}
    window["slots"] = sched                      # đóng băng lịch: các bước sau chỉ đọc lại, không tính lại
    return {"lp_window": window, "lp_tasks": make_tasks(window, state["student_model"]), "lp_results": {},
            "lp_issues": {}, "lp_revision_count": 0, "current_step": "learning_path"}