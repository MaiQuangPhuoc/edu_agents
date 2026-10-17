import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state_plan import PlanState
from src.clients.llm import LLMClient
from src.edu_planning.lp_assemble import phase_weeks
from src.edu_planning.lp_review import review
from src.edu_planning.lp_tools import _build_schedule


def check_week(week: dict, brief: dict, n_slots: int) -> list[str]:
    """Kiểm tra bằng code: số buổi, bài hợp lệ, phủ đủ bài, buổi kiểm tra."""
    ss, issues = week.get("sessions", []), []
    if len(ss) != n_slots:
        issues.append(f"Cần đúng {n_slots} buổi, đang có {len(ss)}")
    want = {(l["chapter_id"], l["lesson"]) for l in brief["lessons"]}
    for s in ss:
        tag = f"{s['date']} {s['start_time']}"
        if not s["chapter_id"]:
            issues.append(f"{tag}: mã bài '{s['lesson']}' không hợp lệ")
        elif s["type"] == "lesson" and (s["chapter_id"], s["lesson"]) not in want:
            issues.append(f"{tag}: bài {s['chapter_id']} - {s['lesson']} không thuộc khung của tuần")
        if not s["activities"]:
            issues.append(f"{tag}: chưa có hoạt động")
    n_learn = n_slots - (1 if brief["has_assessment"] else 0)
    got = {(s["chapter_id"], s["lesson"]) for s in ss if s["type"] != "assessment"}
    if want and len(want) <= n_learn and want - got:       # đủ buổi mà vẫn thiếu bài thì mới báo
        issues.append("Chưa có buổi học các bài: " + ", ".join(sorted(l for _, l in want - got)))
    last_is_test = bool(ss) and ss[-1]["type"] == "assessment"
    if brief["has_assessment"] and ss and not last_is_test:
        issues.append("Buổi cuối tuần phải là assessment")
    if not brief["has_assessment"] and any(s["type"] == "assessment" for s in ss):
        issues.append("Tuần này không có kiểm tra, không được dùng assessment")
    return issues


def critic_node(state: PlanState, llm_client: LLMClient) -> dict:
    print(">>> [LP] critic")
    draft, w = state.get("lp_draft", {}), state["lp_window"]
    if not draft or "error" in draft:
        return {"lp_issues": {}}

    sched = _build_schedule(state["student_model"], w["subject"], w)
    slots = {sw["week_no"]: len(sw["sessions"]) for sw in sched["weeks"]}
    briefs = {b["week_no"]: b for b in phase_weeks(state)}
    evidence = "\n".join(r["evidence"] for r in state["lp_results"].values())

    issues = {}
    for wk in draft["weeks"]:
        for s in wk["sessions"]:                        # bỏ tài nguyên có url không xuất hiện trong kết quả tra cứu
            s["resources"] = [r for r in s["resources"] if r.get("url") and r["url"] in evidence]
        found = check_week(wk, briefs[wk["week_no"]], slots[wk["week_no"]])
        if found:
            issues[str(wk["week_no"])] = found

    revision, reviewed = state.get("lp_revision_count", 0), state.get("lp_reviewed", False)
    if not issues and not reviewed:                     # lớp 2: LLM đối chiếu hồ sơ, chỉ chạy một lần
        reviewed = True
        for week_no, problem in review(state, draft, llm_client):
            if week_no in briefs:
                issues.setdefault(str(week_no), []).append(problem)
            else:
                draft["assumptions"].append("Cần xem lại: " + problem)
    return {"lp_draft": draft, "lp_issues": issues, "lp_reviewed": reviewed,
            "lp_revision_count": revision + (1 if issues else 0)}