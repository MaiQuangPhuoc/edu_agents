"""Tạo bài ôn tập cho MỘT buổi học: LLM (120b) điền yêu cầu thay học sinh, rồi chạy edu_exam ở chế độ tự động."""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import json
from pathlib import Path
from pydantic import BaseModel, Field
from src.state_plan import HandoffMessage
from src.clients.llm import LLMClient, build_prompt_messages
from src.edu_qa.paths import EXAM_COLLECT_AUTO_PROMPT_PATH, TEST_EXAM_PROMPT_PATH
from src.edu_exam.curriculum import get_chapter
from src.edu_exam.exercise_search import find_tests, tests_text

MIN_Q, MAX_Q = 5, 15


class SectionScore(BaseModel):
    section: str
    score: int = Field(description="0 đến 3")


class ExamRequest(BaseModel):
    so_cau_hoi: int
    thoi_gian_lam_bai: int
    muc_tieu_diem: float
    muc_dich: str
    ghi_chu: str = ""
    section_scores: list[SectionScore]


def _topic(sm: dict, subject: str, chapter_id: str) -> dict:
    nl = next((x for x in sm.get("nang_luc") or [] if x.get("mon_hoc") == subject), {})
    cd = next((t for t in nl.get("chu_de") or [] if str(t.get("chapter_id")) == chapter_id), {})
    return {"nl": nl, "cd": cd}


def _student_brief(sm: dict, subject: str, chapter_id: str) -> str:
    t = _topic(sm, subject, chapter_id)
    goal = next((g for g in sm.get("muc_tieu") or [] if g.get("mon_hoc") == subject), {})
    lines = [f"điểm hiện tại: {t['nl'].get('diem_hien_tai')}", f"điểm mạnh: {t['nl'].get('diem_manh') or '(chưa có)'}",
             f"điểm yếu: {t['nl'].get('diem_yeu') or '(chưa có)'}",
             f"mức nắm chương {chapter_id} (0-1): {t['cd'].get('muc_nam')} (độ tin cậy {t['cd'].get('do_tin_cay')})",
             f"điểm mục tiêu: {goal.get('muc_tieu_diem')}", f"dạng bài muốn giữ: {goal.get('dang_bai_can_giu') or '(không)'}"]
    return "\n".join("- " + x for x in lines)


def _session_brief(s: dict) -> str:
    acts = "; ".join(f"{a.get('type')} {a.get('minutes')}p" + (f" ({a['problem_type']})" if a.get("problem_type") else "")
                     for a in s.get("activities", []))
    return "\n".join(["- ý chính: " + "; ".join(s.get("key_points", [])[:5]), "- cần nhớ: " + "; ".join(s.get("must_know", [])[:6]),
                      f"- độ khó buổi: {s.get('difficulty')}", f"- hoạt động: {acts}"])


def _fallback_score(muc_nam) -> int:
    return 2 if muc_nam is None else 3 if muc_nam < 0.5 else 2 if muc_nam < 0.7 else 1


def _fallback_count(s: dict) -> int:
    ex = sum(a.get("minutes", 0) for a in s.get("activities", []) if a.get("type") == "exercise")
    return min(MAX_Q, max(MIN_Q, ex // 3)) if ex else 10


def collect_request(sm: dict, session: dict, subject: str, llm_client: LLMClient) -> dict:
    """LLM điền yêu cầu; code kiểm tra từng trường, trường nào sai/thiếu thì dùng giá trị dự phòng."""
    cid, lesson = str(session["chapter_id"]), session["lesson"]
    chapter = get_chapter(subject, cid)
    sections = chapter["lessons"].get(lesson)
    if not sections:
        raise ValueError(f"Bài '{lesson}' không có trong chương {cid} của {subject}")
    cd = _topic(sm, subject, cid)["cd"]
    res = None
    try:
        res = llm_client.invoke_structured(ExamRequest, build_prompt_messages(EXAM_COLLECT_AUTO_PROMPT_PATH, {
            "subject": subject, "chapter_name": chapter["chapter_name"], "lesson": lesson,
            "sections": "\n".join(f"- {x}" for x in sections), "student_brief": _student_brief(sm, subject, cid),
            "session_brief": _session_brief(session)}), max_tokens=1500)
    except Exception as e:
        print(f"[exam_collect] LLM lỗi, dùng dự phòng: {type(e).__name__} {str(e)[:100]}")
    got = {x.section: x.score for x in (res.section_scores if res else []) if x.section in sections and 0 <= x.score <= 3}
    if len(got) != len(sections) or not any(got.values()):                 # thiếu section hoặc toàn 0: dùng dự phòng
        print(f"[exam_collect] điểm section từ LLM không dùng được ({len(got)}/{len(sections)}) -> dự phòng theo muc_nam")
        got = {x: _fallback_score(cd.get("muc_nam")) for x in sections}
    n = res.so_cau_hoi if res and MIN_Q <= res.so_cau_hoi <= MAX_Q else _fallback_count(session)
    diem = res.muc_tieu_diem if res and 5 <= res.muc_tieu_diem <= 10 else 7
    note = f"Chỉ ra đề cho bài '{lesson}' (chương {cid} {chapter['chapter_name']}). " + (res.ghi_chu if res else "")
    profile = {"mon_hoc": subject, "khoi_lop": 10, "pham_vi_kiem_tra": f"Chương {cid}", "loai_de": "trắc nghiệm",
               "muc_dich": (res.muc_dich if res and res.muc_dich else "ôn tập sau buổi học"), "so_cau_hoi": n,
               "thoi_gian_lam_bai": res.thoi_gian_lam_bai if res and res.thoi_gian_lam_bai > 0 else n * 2,
               "muc_tieu_diem": diem, "ghi_chu": note.strip()}
    return {"profile": profile, "scores": {cid: {lesson: got}},
            "scope_chapters": {cid: chapter["chapter_name"]}, "scope_lessons": {cid: [lesson]}}


def initial_state(req: dict) -> dict:
    return {"messages": [], "student_profile": req["profile"], "profile_complete": True, "auto_mode": True,
            "scope_chapters": req["scope_chapters"], "scope_lessons": req["scope_lessons"],
            "knowledge_queue": [], "knowledge_pending": None, "knowledge_scores": req["scores"],
            "knowledge_retried": False, "retrieved_chunks": [], "retrieve_complete": False}


def run_exam_for_session(student_model: dict, session: dict, subject: str, llm_client: LLMClient,
                         heavy_client: LLMClient, retriever) -> dict:
    from src.edu_exam.graph_exam_v2 import create_graph             # import muộn: tránh nạp cả graph khi chỉ test từng phần
    req = collect_request(student_model, session, subject, llm_client)
    print(f"[exam_session] yêu cầu: {json.dumps(req['profile'], ensure_ascii=False)}")
    graph = create_graph(llm_client, retriever, heavy_client=heavy_client)
    out = graph.invoke(initial_state(req), {"recursion_limit": 60})
    exam = out.get("final_exam") or out.get("generated_exam") or []
    if not exam:
        raise ValueError("Không tạo được câu hỏi nào")
    lesson = session["lesson"]
    other = [q["id"] for q in exam if q.get("bai") and q["bai"] != lesson]
    if other:
        print(f"[exam_session] cảnh báo: câu {other} thuộc bài khác {lesson}")
    key = Path(TEST_EXAM_PROMPT_PATH) / f"{out.get('exam_id', '')}.json"
    topics = list(dict.fromkeys(q.get("dang_bai", "") for q in exam if q.get("dang_bai")))
    chapter_name = req["scope_chapters"][str(session["chapter_id"])]
    return {"exam": exam, "exam_id": out.get("exam_id", ""), "key_file": str(key) if key.exists() else "",
            "tests": find_tests(subject, chapter_name, lesson, topics)}


def handle_request(msg: dict, llm_client: LLMClient, heavy_client: LLMClient, retriever) -> dict:
    """HandoffMessage(request, payload: student_model, subject, session) -> HandoffMessage(result)."""
    def reply(ok: bool, **p):
        return HandoffMessage(sender="exam", receiver="roadmap", type="result", payload={"ok": ok, **p}).model_dump(mode="json")
    p = msg["payload"]
    try:
        r = run_exam_for_session(p["student_model"], p["session"], p["subject"], llm_client, heavy_client, retriever)
    except Exception as e:
        return reply(False, error=f"{type(e).__name__}: {str(e)[:200]}")
    questions = [{"no": i, "chapter_id": p["session"]["chapter_id"], "question": q["question"], "options": q["options"]}
                 for i, q in enumerate(r["exam"], 1)]
    return reply(True, subject=p["subject"], exam_id=r["exam_id"], key_file=r["key_file"], questions=questions,
                 tests=r["tests"], tests_text=tests_text(r["tests"]))


def run_for_enabled_session(out: dict, llm_client: LLMClient, retriever) -> dict | None:
    """Chạy thử sau khi có lộ trình: tạo bài ôn tập cho buổi có exam_enabled = true, in kết quả ra terminal."""
    from src.configs import env_config
    lp = out.get("learning_path") or {}
    session = next((s for w in lp.get("weeks", []) for s in w.get("sessions", []) if s.get("exam_enabled")), None)
    if not session:
        print(">>> Không có buổi nào bật exam_enabled, bỏ qua tạo bài ôn tập")
        return None
    sm = out["student_model"]
    subject = (out.get("lp_window") or {}).get("subject") or sm["muc_tieu"][0]["mon_hoc"]
    heavy = LLMClient(model=env_config.model_edu_exam, api_provider=env_config.plan_provider)
    print(f">>> Tạo bài ôn tập: {subject} | chương {session['chapter_id']} | {session['lesson']} | {session['date']}")
    res = handle_request({"payload": {"student_model": sm, "subject": subject, "session": session}}, llm_client, heavy, retriever)["payload"]
    if not res["ok"]:
        print(">>> Tạo bài ôn tập lỗi:", res["error"])
        return res
    print(f"\n===== BÀI ÔN TẬP ({len(res['questions'])} câu) | mã đề {res['exam_id']} =====")
    for q in res["questions"]:
        print(f"\nCâu {q['no']}: {q['question']}")
        for k, v in q["options"].items():
            print(f"  {k}. {v}")
    print("\nFile đáp án:", res["key_file"] or "(không tìm thấy)")
    print("\n" + (res["tests_text"] or "Không tìm được bài tập tham khảo trên mạng."))
    return res
