import json
from src.state_plan import PlanState, TaskPlan
from src.clients.llm import LLMClient
from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_qa.paths import LP_PLANNER_PROMPT_PATH
from src.edu_planning.lp_tools import _build_schedule

MAX_WINDOW_CHAPTERS = 2      # số chương tối đa trong cửa sổ chi tiết (quy tắc tự đặt)
MAX_GENERATED = 3


def build_window(state: PlanState) -> dict:
    phases = state.get("master_roadmap", {}).get("giai_doan", [])
    order = state.get("vi_tri_hien_tai") or 1
    phase = next((p for p in phases if p["thu_tu"] == order), phases[0] if phases else {})
    chapters = phase.get("chapters", [])[:MAX_WINDOW_CHAPTERS]
    return {
        "start_date": None, "num_weeks": 1, "first_week_no": 1,
        "phase": phase.get("thu_tu", order), "phase_name": phase.get("ten", ""),
        "phase_goal": phase.get("muc_tieu", ""), "subject": phase.get("mon_hoc", ""),
        "chapter_ids": [c["chapter_id"] for c in chapters],
        "chapter_lessons": {c["chapter_id"]: c["lessons"] for c in chapters},
    }


def window_text(w: dict) -> str:
    cur = get_subject_curriculum(w["subject"])
    lines = [f"Môn: {w['subject']} | Giai đoạn {w['phase']}: {w['phase_name']} | Mục tiêu: {w['phase_goal']}",
             f"Cửa sổ chi tiết: {w['num_weeks']} tuần. Các chương:"]
    for cid in w["chapter_ids"]:
        lines.append(f"- chapter_id={cid}: {cur.get(cid, {}).get('chapter_name', '')} | bài: {', '.join(w['chapter_lessons'][cid])}")
    return "\n".join(lines)


def student_text(sm: dict) -> str:
    return json.dumps({k: v for k, v in sm.items() if k != "tien_do"}, ensure_ascii=False, indent=2)


def fixed_tasks(w: dict) -> list[dict]:
    ids = ", ".join(w["chapter_ids"])
    return [
        {"id": "F1", "origin": "fixed", "depends_on": [],
         "goal": f"Nắm kiến thức cần dạy của các chương {ids} (kiến thức chính, cần nắm, cần hiểu, dạng bài, liên hệ giữa các bài)."},
        {"id": "F2", "origin": "fixed", "depends_on": [],
         "goal": "Xác định các buổi học cụ thể trong tuần và độ khó phù hợp theo mục tiêu điểm."},
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
    w = state["lp_window"]
    sched = _build_schedule(state["student_model"], w["subject"], w)
    if "error" in sched:
        gaps.append("Lịch học: " + sched["error"])
    else:
        gaps += [f"Lịch học: {x}" for x in sched["warnings"] if "chỉ xếp được" in x or "vượt quá" in x]
    return gaps


def plan_node(state: PlanState, llm_client: LLMClient) -> dict:
    print(">>> [LP] plan")
    window = build_window(state)
    tasks = fixed_tasks(window)
    tasks += _generate({**state, "lp_window": window}, llm_client, tasks, "(không có)")
    return {"lp_window": window, "lp_tasks": tasks, "lp_results": {}, "lp_replan_count": 0,
            "lp_issues": {}, "lp_revision_count": 0, "current_step": "learning_path"}


def replan_node(state: PlanState, llm_client: LLMClient) -> dict:
    print(">>> [LP] replan")
    new = _generate(state, llm_client, state["lp_tasks"], "\n".join(find_gaps(state)))
    return {"lp_tasks": state["lp_tasks"] + new, "lp_replan_count": state.get("lp_replan_count", 0) + 1}