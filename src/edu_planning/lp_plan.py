import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state_plan import PlanState, TaskPlan
from src.clients.llm import LLMClient
from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_qa.paths import LP_PLANNER_PROMPT_PATH
from src.edu_planning.lp_tools import _build_schedule
from src.edu_planning.chapter_utils import normalize_chapter_id

MAX_WINDOW_CHAPTERS = 2      # số chương tối đa trong cửa sổ chi tiết (quy tắc tự đặt)
MAX_GENERATED = 3


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


def fixed_tasks(w: dict) -> list[dict]:
    ids = ", ".join(w["chapter_ids"])
    return [
        {"id": "F1", "origin": "fixed", "depends_on": [],
         "goal": f"Nắm kiến thức cần dạy của các chương {ids} (kiến thức chính, cần nắm, cần hiểu, dạng bài, liên hệ giữa các bài)."}
    ]


def _generate(state: PlanState, llm_client: LLMClient, existing: list[dict], replan: str) -> list[dict]:
    w = state["lp_window"]
    prompt = (LP_PLANNER_PROMPT_PATH.read_text(encoding="utf-8")
              .replace("{student_model}", student_text(state["student_model"]))
              .replace("{window}", window_text(w))
              .replace("{fixed_tasks}", "\n".join(f"{t['id']}: {t['goal']}" for t in existing))
              .replace("{replan}", replan))
    try:
        plan = llm_client.invoke_structured(TaskPlan, [{"role": "user", "content": prompt}], max_tokens=1500)
    except Exception as e:
        print(f"[lp_plan] lỗi: {e}")
        plan = None
    if plan is None:
        return []

    known = {t["id"] for t in existing}
    start = sum(t["origin"] == "generated" for t in existing)
    out = []
    for i, t in enumerate(plan.tasks[:MAX_GENERATED], start + 1):
        t = t.model_dump()
        t.update(id=f"g{i}", origin="generated", depends_on=[d for d in t["depends_on"] if d in known])
        known.add(t["id"])      # chỉ cho phép phụ thuộc bước đã có trước đó => không có vòng
        out.append(t)
    return out


def find_gaps(state: PlanState) -> list[str]:
    gaps = [f"{tid} ({r['goal']}): {r['text'][:200]}"
            for tid, r in state.get("lp_results", {}).items() if "THIẾU" in r["text"]]
    
    return gaps


def plan_node(state: PlanState, llm_client: LLMClient) -> dict:
    print(">>> [LP] plan")
    window = build_window(state)

    sched = _build_schedule(state["student_model"], window["subject"], window)
    if "error" in sched:
        return {"lp_draft": {"error": sched["error"]}}
    window["slots"] = sched                      # đóng băng lịch: các bước sau chỉ đọc lại, không tính lại
    tasks = fixed_tasks(window)
    tasks += _generate({**state, "lp_window": window}, llm_client, tasks, "(không có)")
    return {"lp_window": window, "lp_tasks": tasks, "lp_results": {}, "lp_replan_count": 0,
            "lp_issues": {}, "lp_revision_count": 0, "current_step": "learning_path"}


def replan_node(state: PlanState, llm_client: LLMClient) -> dict:
    print(">>> [LP] replan")
    new = _generate(state, llm_client, state["lp_tasks"], "\n".join(find_gaps(state)))
    return {"lp_tasks": state["lp_tasks"] + new, "lp_replan_count": state.get("lp_replan_count", 0) + 1}