import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state_plan import PlanState, ReviewResult
from src.clients.llm import LLMClient
from src.edu_qa.paths import LP_REVIEW_PROMPT_PATH
from src.edu_planning.lp_plan import student_text
from src.clients.llm import LLMClient, build_prompt_messages

def summary_text(state: PlanState, draft: dict) -> str:
    """Bản rút gọn: mỗi tuần một dòng, tuần chi tiết có thêm mỗi buổi một dòng."""
    rev = {(v["chapter_id"], v["lesson"]): k for k, v in state["lp_codes"].items()}
    detail = {wk["week_no"]: wk for wk in draft.get("weeks", [])}
    lines = []
    for o in state["lp_outline"]:
        for b in o["weeks"]:
            codes = ", ".join(rev.get((l["chapter_id"], l["lesson"]), "?") for l in b["lessons"])
            lines.append(f"Tuần {b['week_no']} (giai đoạn {o['phase']}) | {b['goal']} | {b['difficulty_trend']} | "
                         f"{b['total_hours']}h | kiểm tra: {'có' if b['has_assessment'] else 'không'} | bài: {codes}")
            for i, s in enumerate(detail.get(b["week_no"], {}).get("sessions", []), 1):
                acts = ", ".join(f"{a['type']} {a['minutes']}" for a in s["activities"])
                lines.append(f"  Buổi {i} ({s['minutes']}p, {s['type']}, {s['difficulty']}): "
                             f"{rev.get((s['chapter_id'], s['lesson']), '?')} {s['lesson']} | {acts} | tài nguyên: {len(s['resources'])}")
    return "\n".join(lines)


def review(state: PlanState, draft: dict, llm_client: LLMClient) -> list[tuple[int, str]]:
    """Trả [(week_no, nội dung)]. week_no > 0: critic soạn lại tuần đó; week_no = 0: chỉ ghi chú vào assumptions."""
    messages = build_prompt_messages(LP_REVIEW_PROMPT_PATH, {
        "student_model": student_text(state["student_model"]),
        "summary": summary_text(state, draft)})
    try:
        res = llm_client.invoke_structured(ReviewResult, messages, max_tokens=3000)
    except Exception as e:
        print(f"[lp_review] lỗi: {e}")
        return []
    if res is None:
        return []
    out = []
    for i in res.issues:
        if not i.evidence.strip() or not i.fix.strip():           # phê bình không dẫn chứng hoặc không có cách sửa thì bỏ
            continue
        text = f"{i.fix} (căn cứ: {i.evidence})"
        fixable = res.verdict == "revise" and i.severity != "low" and i.week_no > 0
        out.append((i.week_no if fixable else 0, text))
    return out