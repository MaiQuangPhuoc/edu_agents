
import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_planning.lp_tools import _build_schedule
from src.state_plan import PlanState

def _slots(sessions: list[dict]) -> set:
    return {(s["date"], s["start_time"], s["minutes"]) for s in sessions}


def check_week(week: dict, sched_week: dict, w: dict) -> list[str]:
    issues = []
    sessions = sorted(week.get("sessions", []), key=lambda s: (s["date"], s["start_time"]))
    if _slots(sessions) != _slots(sched_week["sessions"]):
        issues.append(f"Buổi học không khớp lịch chính xác. Cần: {sorted(_slots(sched_week['sessions']))}. "
                      f"Đang có: {sorted(_slots(sessions))}")
    cur = get_subject_curriculum(w["subject"])
    for s in sessions:
        tag = f"{s['date']} {s['start_time']}"
        if s["chapter_id"] not in w["chapter_ids"]:
            issues.append(f"{tag}: chapter_id {s['chapter_id']} nằm ngoài cửa sổ")
        elif s["lesson"] not in cur[s["chapter_id"]]["lessons"]:
            issues.append(f"{tag}: bài '{s['lesson']}' không có trong chương {s['chapter_id']}")
        total = sum(a["minutes"] for a in s["activities"])
        if total != s["minutes"]:
            issues.append(f"{tag}: tổng thời lượng hoạt động {total} phút, cần {s['minutes']} phút")
    if sessions and sessions[-1]["type"] != "assessment":
        issues.append("Buổi cuối tuần phải có type = assessment")
    return issues


def critic_node(state: PlanState) -> dict:
    print(">>> [LP] critic")
    draft, w = state.get("lp_draft", {}), state["lp_window"]
    if not draft or "error" in draft:
        return {"lp_issues": {}}

    sched = _build_schedule(state["student_model"], w["subject"], w)
    by_week = {sw["week_no"]: sw for sw in sched["weeks"]}
    evidence = "\n".join(r["evidence"] for r in state["lp_results"].values())

    issues = {}
    for wk in draft["weeks"]:
        for s in wk.get("sessions", []):                   # bỏ tài nguyên có url không xuất hiện trong kết quả tra cứu
            s["resources"] = [r for r in s["resources"] if r.get("url") and r["url"] in evidence]
        found = check_week(wk, by_week[wk["week_no"]], w)
        if found:
            issues[str(wk["week_no"])] = found

    count = state.get("lp_revision_count", 0) + (1 if issues else 0)
    return {"lp_draft": draft, "lp_issues": issues, "lp_revision_count": count}