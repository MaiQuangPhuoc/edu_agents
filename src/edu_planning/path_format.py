"""Đổi lộ trình (JSON/dict theo schema LearningPath) sang văn bản. Chỉ là code, không gọi LLM."""

_KIND = {"lesson": "Học bài", "review": "Ôn tập", "assessment": "Kiểm tra"}
_ACT = {"lecture": "Nghe giảng", "reading": "Đọc tài liệu", "video": "Xem video",
        "exercise": "Làm bài tập", "summary": "Tóm tắt", "review": "Ôn lại"}


def _cell(text) -> str:
    return str(text).replace("|", "/").replace("\n", " ")


def _outline(outline: list[dict]) -> list[str]:
    out = []
    for o in outline:
        out += ["", f"### Giai đoạn {o['phase']}", "",
                "| Tuần | Mục tiêu | Bài | Độ khó | Giờ | Kiểm tra |", "|---|---|---|---|---|---|"]
        for b in o["weeks"]:
            lessons = "; ".join(f"{l['chapter_id']}: {l['lesson']}" for l in b["lessons"])
            out.append(f"| {b['week_no']} | {_cell(b['goal'])} | {_cell(lessons)} | {_cell(b['difficulty_trend'])} "
                       f"| {b['total_hours']} | {'có' if b['has_assessment'] else ''} |")
    return out


def _session(s: dict) -> list[str]:
    out = ["", f"#### {s['date']} {s['start_time']} · {s['minutes']} phút · {_KIND.get(s['type'], s['type'])} · độ khó {s['difficulty']}",
           f"**Chương {s['chapter_id']} — {s['lesson']}**", ""]
    for title, key in (("Ý chính", "key_points"), ("Cần nắm", "must_know"), ("Cần hiểu", "must_understand")):
        if s[key]:
            out.append(f"- {title}: " + "; ".join(s[key]))
    if s["related"]:
        out.append("- Liên hệ: " + "; ".join(f"{r['lesson']} (chương {r['chapter_id']}, {r['relation']})" for r in s["related"]))
    out += ["", "Hoạt động:"]
    for a in s["activities"]:
        extra = f" — dạng bài: {a['problem_type']}" if a.get("problem_type") else ""
        out.append(f"- {_ACT.get(a['type'], a['type'])} ({a['minutes']} phút, {a['difficulty']}): {a['content']}{extra}")
    if s["resources"]:
        out += ["", "Tài nguyên:"]
        out += [f"- [{r['title']}]({r['url']})" if r.get("url") else f"- {r['title']}" for r in s["resources"]]
    if s.get("assessment"):
        a = s["assessment"]
        out += ["", f"Bài test: {a['num_questions']} câu, chương {', '.join(a['chapter_ids'])}"]
    return out


def to_markdown(lp: dict) -> str:
    sc = lp["schedule"]
    lines = [f"# Lộ trình học chi tiết (giai đoạn {lp['current_phase']})", "",
             f"- Bắt đầu: {sc['start_date']}" + (f" · Hạn: {sc['end_date']}" if sc.get("end_date") else ""),
             f"- {sc['sessions_per_week']} buổi mỗi tuần, mỗi buổi {sc['minutes_per_session']} phút · tổng {sc['total_weeks']} tuần"]
    if lp.get("assumptions"):
        lines += ["", "## Lưu ý"] + [f"- {a}" for a in lp["assumptions"]]
    lines += ["", "## Tổng quan các giai đoạn"] + _outline(lp.get("outline", []))
    lines += ["", f"## Chi tiết giai đoạn {lp['current_phase']}"]
    for wk in lp["weeks"]:
        lines += ["", f"### Tuần {wk['week_no']} ({wk['start_date']} → {wk['end_date']}): {wk['goal']}"]
        if not wk["sessions"]:
            lines.append("_Chưa xếp được buổi học trong tuần này._")
        for s in wk["sessions"]:
            lines += _session(s)
    return "\n".join(lines) + "\n"