import json
import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state_plan import PlanState, Week
from src.clients.llm import LLMClient
from src.edu_qa.paths import LP_ASSEMBLE_PROMPT_PATH
from src.edu_planning.lp_plan import window_text, student_text
from src.edu_planning.lp_tools import _build_schedule
from src.edu_planning.chapter_utils import normalize_chapter_id

def _results_text(results: dict, sched_week: dict) -> str:
    body = "\n\n".join(f"[{tid}] {r['goal']}\n{r['text']}" for tid, r in results.items())
    exact = json.dumps(sched_week["sessions"], ensure_ascii=False)
    return body + f"\n\n[LỊCH CHÍNH XÁC TUẦN {sched_week['week_no']}]\n{exact}"


def _assemble_week(state: PlanState, llm_client: LLMClient, sw: dict, issues: list[str]) -> dict:
    prompt = (LP_ASSEMBLE_PROMPT_PATH.read_text(encoding="utf-8")
              .replace("{week_no}", str(sw["week_no"]))
              .replace("{student_model}", student_text(state["student_model"]))
              .replace("{window}", window_text(state["lp_window"]))
              .replace("{results}", _results_text(state["lp_results"], sw))
              .replace("{issues}", "\n".join(f"- {i}" for i in issues) or "(không có)"))
    try:
        week = llm_client.invoke_structured(Week, [{"role": "user", "content": prompt}], max_tokens=6000)
    except Exception as e:
        print(f"[lp_assemble] tuần {sw['week_no']} lỗi: {e}")
        week = None
    data = week.model_dump() if week else {"goal": "", "sessions": []}
    subject = state["lp_window"]["subject"]
    for s in data["sessions"]:
        s["chapter_id"] = normalize_chapter_id(subject, s["chapter_id"]) or s["chapter_id"]
    data.update(week_no=sw["week_no"], start_date=sw["start_date"], end_date=sw["end_date"])
    return data


def assemble_node(state: PlanState, llm_client: LLMClient) -> dict:
    print(">>> [LP] assemble")
    w = state["lp_window"]
    sched = _build_schedule(state["student_model"], w["subject"], w)
    if "error" in sched:
        return {"lp_draft": {"error": sched["error"]}, "lp_issues": {}}

    old = {wk["week_no"]: wk for wk in state.get("lp_draft", {}).get("weeks", [])}
    issues = state.get("lp_issues") or {}
    weeks = []
    for sw in sched["weeks"]:
        n = sw["week_no"]
        if n in old and not issues.get(str(n)):            # giữ tuần đã đạt, chỉ làm lại tuần có lỗi
            weeks.append(old[n])
        else:
            weeks.append(_assemble_week(state, llm_client, sw, issues.get(str(n), [])))

    schedule = {"start_date": sched["start_date"], "end_date": sched["deadline"],
                "total_weeks": sched["weeks_remaining"] or w["num_weeks"],
                "sessions_per_week": sched["sessions_per_week"], "minutes_per_session": sched["minutes_per_session"]}
    return {"lp_draft": {"current_phase": w["phase"], "schedule": schedule, "weeks": weeks, "assumptions": []}}