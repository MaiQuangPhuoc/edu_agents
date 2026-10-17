import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from concurrent.futures import ThreadPoolExecutor
from src.state_plan import PlanState, WeekDraft
from src.clients.llm import LLMClient
from src.edu_qa.paths import LP_ASSEMBLE_PROMPT_PATH
from src.edu_planning.lp_plan import student_text
from src.edu_planning.lp_tools import _build_schedule
from src.edu_planning.lp_finalize import build_week, assessment_scopes

MAX_WORKERS = 3


def phase_weeks(state: PlanState) -> list[dict]:
    """Các tuần mức vừa của giai đoạn hiện tại."""
    return next(o["weeks"] for o in state["lp_outline"] if o["phase"] == state["lp_window"]["phase"])


def _brief_text(b: dict) -> str:
    return (f"mục tiêu: {b['goal']}; hoạt động: {', '.join(b['activity_types']) or '(tùy)'}; "
            f"độ khó: {b['difficulty_trend'] or '(tùy)'}; {b['total_hours']} giờ; "
            f"kiểm tra cuối tuần (has_assessment): {str(b['has_assessment']).lower()}")


def _lessons_text(b: dict, state: PlanState) -> str:
    rev = {(v["chapter_id"], v["lesson"]): k for k, v in state["lp_codes"].items()}
    lines = []
    for l in b["lessons"]:
        ch = state.get("lp_knowledge", {}).get(l["chapter_id"]) or {}
        kn = next((x for x in ch.get("lessons", []) if x.get("lesson") == l["lesson"]), {})
        lines.append(f"{rev.get((l['chapter_id'], l['lesson']), '?')}: {l['lesson']} — " + "; ".join(kn.get("key_points", [])[:3]))
    return "\n".join(lines)


def _resources_text(results: dict) -> str:
    parts = [f"[{tid}] {r['text'][:1500]}" for tid, r in results.items() if tid.startswith("g")]
    return "\n".join(parts) or "(không có)"


def _draft_week(state: PlanState, llm_client: LLMClient, sw: dict, brief: dict, issues: list[str]):
    slots = "\n".join(f"Buổi {i}: {s['minutes']} phút" for i, s in enumerate(sw["sessions"], 1))
    prompt = (LP_ASSEMBLE_PROMPT_PATH.read_text(encoding="utf-8")
              .replace("{week_no}", str(sw["week_no"]))
              .replace("{student_model}", student_text(state["student_model"]))
              .replace("{week_outline}", _brief_text(brief))
              .replace("{lessons_info}", _lessons_text(brief, state))
              .replace("{resources}", _resources_text(state.get("lp_results", {})))
              .replace("{slots}", slots)
              .replace("{issues}", "\n".join(f"- {i}" for i in issues) or "(không có)"))
    try:
        return llm_client.invoke_structured(WeekDraft, [{"role": "user", "content": prompt}], max_tokens=3000)
    except Exception as e:
        print(f"[lp_assemble] tuần {sw['week_no']} lỗi: {e}")
        return None


def assemble_node(state: PlanState, llm_client: LLMClient) -> dict:
    print(">>> [LP] assemble")
    w = state["lp_window"]
    sched = _build_schedule(state["student_model"], w["subject"], w)         # lịch đã đóng băng
    if "error" in sched:
        return {"lp_draft": {"error": sched["error"]}, "lp_issues": {}}

    briefs = {b["week_no"]: b for b in phase_weeks(state)}
    ctx = {"codes": state["lp_codes"], "knowledge": state.get("lp_knowledge", {}), "scopes": assessment_scopes(list(briefs.values()))}
    old = {wk["week_no"]: wk for wk in state.get("lp_draft", {}).get("weeks", [])}
    issues = state.get("lp_issues") or {}
    todo = [sw for sw in sched["weeks"] if not (sw["week_no"] in old and not issues.get(str(sw["week_no"])))]

    def work(sw):
        n = sw["week_no"]
        draft = _draft_week(state, llm_client, sw, briefs[n], issues.get(str(n), [])) if sw["sessions"] else None
        return n, build_week(draft, briefs[n], sw, ctx)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        new = dict(ex.map(work, todo))
    weeks = [new.get(sw["week_no"]) or old[sw["week_no"]] for sw in sched["weeks"]]      # giữ tuần đã đạt

    notes = [a for a in state.get("lp_draft", {}).get("assumptions", []) if a.startswith("Cần xem lại")]   # ghi chú của review
    schedule = {"start_date": sched["start_date"], "end_date": sched["deadline"],
                "total_weeks": sched["weeks_remaining"] or w["num_weeks"],
                "sessions_per_week": sched["sessions_per_week"], "minutes_per_session": sched["minutes_per_session"]}
    return {"lp_draft": {"current_phase": w["phase"], "schedule": schedule, "outline": state["lp_outline"],
                         "weeks": weeks, "assumptions": list(sched["warnings"]) + notes}}