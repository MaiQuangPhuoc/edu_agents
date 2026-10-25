import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import date
from src.state_plan import PlanState, OutlinePlan
from src.clients.llm import LLMClient, build_prompt_messages
from src.edu_qa.paths import LP_OUTLINE_PROMPT_PATH
from src.edu_planning.chapter_utils import normalize_chapter_id
from src.edu_planning.lp_plan import phases_in_scope, student_text
from src.edu_planning.lp_tools import _pick_goal, _deadline, _DIFFICULTY_RATIO, DEFAULT_TARGET_SCORE
from src.edu_planning.lp_time import time_facts_text

MAX_TRIES = 3


def build_codes(subject: str, phases: list[dict]) -> dict:
    """Mã bài duy nhất: '{chapter_id}.{số thứ tự}' -> {phase, chapter_id, lesson}."""
    codes, count = {}, {}
    for p in phases:
        for c in p.get("chapters", []):
            cid = normalize_chapter_id(subject, c["chapter_id"]) or str(c["chapter_id"])
            for lesson in c["lessons"]:
                count[cid] = count.get(cid, 0) + 1
                codes[f"{cid}.{count[cid]}"] = {"phase": p["thu_tu"], "chapter_id": cid, "lesson": lesson}
    return codes


def roadmap_text(phases: list[dict], codes: dict) -> str:
    lines = []
    for p in phases:
        lines.append(f"Giai đoạn {p['thu_tu']}: {p.get('ten', '')} - {p.get('muc_tieu', '')}")
        lines += [f"  {k}: {v['lesson']}" for k, v in codes.items() if v["phase"] == p["thu_tu"]]
    return "\n".join(lines)


def _time_facts(sm: dict, subject: str):
    lich, st = sm.get("lich_hoc") or {}, sm.get("so_thich_hoc") or {}
    _, weeks = _deadline(_pick_goal(sm, subject), date.today())
    per_week, minutes = lich.get("so_buoi_tuan"), st.get("thoi_luong_buoi_phut")
    return (int(weeks), int(per_week), int(minutes)) if weeks and per_week and minutes else None

def _difficulty_text(sm: dict, subject: str) -> str:
    """Tỉ lệ độ khó mục tiêu theo điểm mục tiêu (bảng cố định trong lp_tools)."""
    score, note = _pick_goal(sm, subject).get("muc_tieu_diem"), ""
    if score is None:
        score, note = DEFAULT_TARGET_SCORE, " (hồ sơ chưa có điểm mục tiêu, tạm dùng mức này)"
    e, m, h = _DIFFICULTY_RATIO[min(max(int(round(score)), 5), 10)]
    return f"mục tiêu {score} điểm: dễ {e:.0%}, vừa {m:.0%}, khó {h:.0%}{note}"

def validate(weeks: list, codes: dict, phases: list[dict], total: int) -> list[str]:
    issues, order = [], [p["thu_tu"] for p in phases]
    seq = [w.phase for w in weeks]
    if len(weeks) != total:
        issues.append(f"Cần đúng {total} tuần, đang có {len(weeks)}")
    if seq != sorted(seq) or set(seq) != set(order):
        issues.append(f"Giai đoạn phải đủ {order}, mỗi giai đoạn ít nhất 1 tuần, xếp liền nhau theo thứ tự")
    seen = {}
    for i, w in enumerate(weeks, 1):
        for c in w.lessons:
            info = codes.get(c)
            if not info:
                issues.append(f"Tuần {i}: mã bài '{c}' không tồn tại")
            elif info["phase"] != w.phase:
                issues.append(f"Tuần {i}: bài {c} thuộc giai đoạn {info['phase']}, không phải {w.phase}")
            elif c in seen and "review" not in w.activity_types:
                issues.append(f"Bài {c} học lặp ở tuần {seen[c]} và tuần {i} (chỉ lặp được ở tuần có review)")
            seen.setdefault(c, i)
    missing = [c for c in codes if c not in seen]
    if missing:
        issues.append("Thiếu bài: " + ", ".join(missing))
    for p in order:
        last = [w for w in weeks if w.phase == p][-1:]
        if last and not last[0].has_assessment:
            issues.append(f"Tuần cuối giai đoạn {p} cần has_assessment = true")
    return issues[:8]


def to_outline(weeks: list, codes: dict, per_week: int, minutes: int) -> list[dict]:
    hours, out = round(per_week * minutes / 60, 1), {}
    for i, w in enumerate(weeks, 1):
        out.setdefault(w.phase, []).append({
            "week_no": i, "goal": w.goal, "activity_types": w.activity_types,
            "difficulty_trend": w.difficulty_trend, "total_hours": hours, "has_assessment": w.has_assessment,
            "lessons": [{"chapter_id": codes[c]["chapter_id"], "lesson": codes[c]["lesson"]} for c in w.lessons]})
    return [{"phase": p, "weeks": ws} for p, ws in out.items()]


def outline_node(state: PlanState, retriever, llm_client: LLMClient) -> dict:
    print(">>> [LP] outline")
    reset = {"lp_draft": {}, "lp_issues": {}, "lp_revision_count": 0, "lp_reviewed": False}      # xóa kết quả của lần chạy trước
    
    fail = lambda msg: {**reset, "lp_draft": {"error": msg}}

    phases = phases_in_scope(state)
    if not phases:
        return fail("Sườn lộ trình chưa có giai đoạn nào")
    subject, sm = phases[0]["mon_hoc"], state["student_model"]
    facts = _time_facts(sm, subject)
    if not facts:
        return fail("Hồ sơ thiếu số tuần còn lại (ngay_ket_thuc hoặc so_tuan_con_lai), số buổi mỗi tuần hoặc thời lượng buổi")
    total, per_week, minutes = facts
    if total < len(phases):
        return fail(f"Chỉ còn {total} tuần, ít hơn số giai đoạn ({len(phases)})")

    codes, issues, plan = build_codes(subject, phases), [], None
    time_facts = time_facts_text(retriever, subject, phases, total, per_week, minutes)
    for attempt in range(MAX_TRIES):
        messages = build_prompt_messages(LP_OUTLINE_PROMPT_PATH, {
            "student_model": student_text(sm),
            "roadmap": roadmap_text(phases, codes),
            "total_weeks": total, "sessions_per_week": per_week,
            "difficulty": _difficulty_text(sm, subject),
            "time_facts": time_facts,
            "issues": "\n".join(f"- {i}" for i in issues) or "(không có)"})
        try:
            plan = llm_client.invoke_structured(OutlinePlan, messages, max_tokens=6000)
        except Exception as e:
            print(f"[lp_outline] lỗi: {e}")
            plan = None
        if plan is None:
            issues = ["Kết quả trước không đúng cấu trúc, hãy xuất lại đúng schema"]
            continue
        issues = validate(plan.weeks, codes, phases, total)
        sc = plan.self_check
        failed = [name for name, ok in (("đủ bài", sc.all_lessons_covered), ("giai đoạn liền nhau", sc.phases_contiguous),
                                        ("tỉ lệ độ khó", sc.difficulty_ratio_ok), ("thời gian", sc.time_budget_ok)) if not ok]
        if not issues and failed and attempt < MAX_TRIES - 1:       # mềm: tự kiểm tra báo chưa đạt thì cho làm lại
            issues = [f"Tự kiểm tra chưa đạt ({', '.join(failed)}): " + "; ".join(sc.notes)]
            continue
        if not issues:
            return {**reset, "lp_outline": to_outline(plan.weeks, codes, per_week, minutes), "lp_codes": codes}
    return fail("Không lập được khung tuần hợp lệ: " + "; ".join(issues))