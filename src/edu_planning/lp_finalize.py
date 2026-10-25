"""Ghép bản nháp của LLM (WeekDraft) thành Week đầy đủ. Toàn bộ là code: chép dữ liệu, không sinh nội dung."""
import re

_LEVEL = {"dễ": "easy", "vừa": "medium", "khó": "hard", "easy": "easy", "medium": "medium", "hard": "hard"}


def levels_for(trend: str, n: int) -> list[str]:
    """'dễ → vừa' + 3 buổi -> ['easy', 'easy', 'medium']. Không hiểu thì 'medium'."""
    toks = [_LEVEL[t] for t in re.findall(r"dễ|vừa|khó|easy|medium|hard", (trend or "").lower())] or ["medium"]
    return [toks[min(len(toks) - 1, i * len(toks) // max(n, 1))] for i in range(n)]


def rescale(mins: list[int], total: int) -> list[int]:
    """Co giãn số phút các hoạt động (bội số 5) để tổng đúng bằng thời lượng buổi."""
    s = sum(mins) or 1
    out = [max(5, round(m * total / s / 5) * 5) for m in mins]
    out[-1] += total - sum(out)
    if min(out) < 5:
        out = [total // len(out)] * len(out)
        out[-1] += total - sum(out)
    return out


def assessment_scopes(brief_weeks: list[dict]) -> dict:
    """{week_no: [chapter_id đã học từ lần kiểm tra trước đến tuần này]} cho các tuần có kiểm tra."""
    scopes, acc = {}, []
    for w in brief_weeks:
        acc += [l["chapter_id"] for l in w["lessons"] if l["chapter_id"] not in acc]
        if w["has_assessment"]:
            scopes[w["week_no"]], acc = acc, []
    return scopes


def _kn(knowledge: dict, chapter_id: str, lesson: str) -> dict:
    ch = knowledge.get(chapter_id) or {}
    return next((x for x in ch.get("lessons", []) if x.get("lesson") == lesson), {})


def build_week(draft, brief: dict, sw: dict, ctx: dict) -> dict:
    """draft: WeekDraft | None; brief: BriefWeek dict; sw: tuần trong lịch đóng băng; ctx: codes, knowledge, scopes."""
    slots = sw["sessions"]
    levels = levels_for(brief.get("difficulty_trend", ""), len(slots))
    sessions = []
    for i, (slot, ds) in enumerate(zip(slots, draft.sessions if draft else [])):
        info = ctx["codes"].get(ds.lesson) or {"chapter_id": "", "lesson": ds.lesson}     # mã sai -> chapter_id rỗng, critic bắt
        kn = _kn(ctx["knowledge"], info["chapter_id"], info["lesson"])
        mins = rescale([a.minutes for a in ds.activities], slot["minutes"]) if ds.activities else []
        types, acts = kn.get("problem_types") or [], []
        for a, m in zip(ds.activities, mins):
            if a.type == "exercise" and types:
                pt = a.problem_type if a.problem_type in types else types[sum(x["type"] == "exercise" for x in acts) % len(types)]
            else:
                pt = ""
            acts.append({"type": a.type, "content": a.content, "minutes": m, "difficulty": levels[i], "problem_type": pt})
        s = {"date": slot["date"], "start_time": slot["start_time"], "minutes": slot["minutes"], "type": ds.type,
             "chapter_id": info["chapter_id"], "lesson": info["lesson"],
             "key_points": kn.get("key_points", []), "must_know": kn.get("must_know", []),
             "must_understand": kn.get("must_understand", []), "related": kn.get("related", []),
             "difficulty": levels[i], "activities": acts,
             "resources": [r.model_dump() for r in ds.resources[:2]], "assessment": None}
        if ds.type == "assessment":
            s["assessment"] = {"chapter_ids": ctx["scopes"].get(brief["week_no"]) or [info["chapter_id"]],
                               "num_questions": min(10, max(5, slot["minutes"] // 10))}
        sessions.append(s)
    return {"week_no": sw["week_no"], "start_date": sw["start_date"], "end_date": sw["end_date"],
            "goal": draft.goal if draft else brief.get("goal", ""), "sessions": sessions}