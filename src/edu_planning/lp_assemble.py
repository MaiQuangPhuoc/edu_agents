import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from concurrent.futures import ThreadPoolExecutor
from src.state_plan import PlanState, WeekDraft
from src.edu_qa.paths import LP_ASSEMBLE_PROMPT_PATH
from src.edu_planning.lp_plan import student_text
from src.edu_planning.lp_tools import _build_schedule
from src.edu_planning.lp_finalize import build_week, assessment_scopes
from src.clients.llm import LLMClient, build_prompt_messages
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
        lines.append(f"{rev.get((l['chapter_id'], l['lesson']), '?')}: {l['lesson']}"
                     f"\n  key_points: " + "; ".join(kn.get("key_points", [])[:4])
                     + "\n  must_know: " + "; ".join(kn.get("must_know", [])[:4])
                     + "\n  must_understand: " + "; ".join(kn.get("must_understand", [])[:3])
                     + "\n  problem_types: " + "; ".join(kn.get("problem_types", [])[:5]))
    return "\n".join(lines)


def _resources_text(results: dict) -> str:
    parts = [f"[{tid}] {r['text'][:1500]}" for tid, r in results.items() if tid.startswith("g")]
    return "\n".join(parts) or "(không có)"

def _draft_week(state: PlanState, llm_client: LLMClient, sw: dict, brief: dict, issues: list[str]):
    slots = "\n".join(f"Buổi {i}: {s['minutes']} phút" for i, s in enumerate(sw["sessions"], 1))
    for attempt in range(2):                      # lần 2 chỉ khi tự kiểm tra báo chưa đạt
        messages = build_prompt_messages(LP_ASSEMBLE_PROMPT_PATH, {
            "week_no": sw["week_no"],
            "student_model": student_text(state["student_model"]),
            "week_outline": _brief_text(brief),
            "lessons_info": _lessons_text(brief, state),
            "resources": _resources_text(state.get("lp_results", {})),
            "slots": slots,
            "issues": "\n".join(f"- {i}" for i in issues) or "(không có)"})
        try:
            draft = llm_client.invoke_structured(WeekDraft, messages, max_tokens=4000)
        except Exception as e:
            print(f"[lp_assemble] tuần {sw['week_no']} lỗi: {e}")
            return None
        if draft is None:
            return None
        sc = draft.self_check
        failed = [name for name, ok in (("số buổi", sc.session_count_matches), ("đủ bài", sc.all_lessons_covered),
                                        ("buổi kiểm tra", sc.assessment_rule_ok), ("tài nguyên", sc.only_given_resources),
                                        ("bám dữ liệu", sc.activities_grounded)) if not ok]
        if not failed or attempt == 1:
            return draft
        issues = list(issues) + [f"Tự kiểm tra chưa đạt ({', '.join(failed)}): " + "; ".join(sc.notes)]
    return draft


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
    notes += [f"Thiếu dữ liệu: {r['goal']}" for r in state.get("lp_results", {}).values() if "THIẾU" in r["text"]]
    schedule = {"start_date": sched["start_date"], "end_date": sched["deadline"],
                "total_weeks": sched["weeks_remaining"] or w["num_weeks"],
                "sessions_per_week": sched["sessions_per_week"], "minutes_per_session": sched["minutes_per_session"]}
    return {"lp_draft": {"current_phase": w["phase"], "schedule": schedule, "outline": state["lp_outline"],
                         "weeks": weeks, "assumptions": list(sched["warnings"]) + notes}}