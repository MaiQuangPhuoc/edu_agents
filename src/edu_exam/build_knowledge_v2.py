import re, json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage
from src.state_edu import ExamState, KnowledgeChapterProfile     # ← thêm KnowledgeChapterProfile
from src.clients.llm import LLMClient
from src.edu_qa.paths import KNOWLEDGE_PROMPT_PATH, ANALYZE_PROMPT_PATH 

from src.edu_exam.curriculum import extract_chapter_ids, get_chapter, get_subject_curriculum

# MESSAGE_TEMPLATE_PATH = Path(r'...\prompt_edu\prompt\build_knowledge.txt')   # giờ chỉ là template, không phải system prompt
# ANALYZE_PROMPT_PATH   = Path(r'...\prompt_edu\prompt\analyze_knowledge.txt')


def _build_queue(profile: dict) -> list:
    subject = profile.get("mon_hoc", "")
    return extract_chapter_ids(profile, subject)


def _build_chapter_section_text(subject: str, ch_id: str) -> str:
    lessons = get_chapter(subject, ch_id)["lessons"]
    lines = []
    for i, (lesson, sections) in enumerate(lessons.items(), 1):
        lines.append(f"Bài {i}: {lesson}")
        for j, sec in enumerate(sections, 1):
            lines.append(f"  {j}. {sec}")
    return "\n".join(lines)


def _parse_scores_chapter(answer: str, subject: str, ch_id: str) -> dict:
    numbers = re.findall(r'[0-3]', answer)
    result, idx = {}, 0
    for lesson, sections in get_chapter(subject, ch_id)["lessons"].items():
        result[lesson] = {}
        for sec in sections:
            result[lesson][sec] = int(numbers[idx]) if idx < len(numbers) else None   # ← None thay vì 0
            idx += 1
    return result


def _find_missing_sections(knowledge_scores: dict) -> list[tuple[str, str, str]]:
    """Quét toàn bộ chương đã hỏi, trả về (ch_id, lesson, section) nào chưa có điểm."""
    missing = []
    for ch_id, lessons in knowledge_scores.items():
        for lesson, sections in lessons.items():
            for sec, score in sections.items():
                if score is None:
                    missing.append((ch_id, lesson, sec))
    return missing


def _analyze_chapters(state: dict, llm_client: LLMClient) -> dict:
    """Phase 2 — LLM DUY NHẤT gọi ở đây, dùng structured output thay vì text tự do."""
    profile          = state.get("student_profile", {})
    retrieved_chunks = state.get("retrieved_chunks", [])
    knowledge_scores = state.get("knowledge_scores", {})
    subject          = profile.get("mon_hoc", "")
    pham_vi          = profile.get("pham_vi_kiem_tra", "")
    ghi_chu          = profile.get("ghi_chu", "không có")

    template          = ANALYZE_PROMPT_PATH.read_text(encoding="utf-8")
    knowledge_profile = {}
    failed_chapters   = []   
    # structured_llm    = llm_client._llm.with_structured_output(KnowledgeChapterProfile)   # ← thêm

    for ch_id, ch_scores in knowledge_scores.items():
        chunks_ch = [
            c["content"]
            for c in retrieved_chunks
            if c["metadata"].get("chapter_id", "") == ch_id       # ← chapter_id, không CHAPTER_MAP
        ]
        chunks_text = "\n---\n".join(chunks_ch[:10])

        scores_text = "\n".join([
            f"  {lesson}:\n" + "\n".join([f"    - {sec}: {score}" for sec, score in sections.items()])
            for lesson, sections in ch_scores.items()
        ])

        prompt = (template
                  .replace("{chuong}",  get_chapter(subject, ch_id)["chapter_name"])
                  .replace("{pham_vi}", str(pham_vi))
                  .replace("{ghi_chu}", str(ghi_chu))
                  .replace("{scores}",  scores_text)
                  .replace("{chunks}",  chunks_text))

        result = None
        for attempt in range(3):
            try:
                # result = structured_llm.invoke([{"role": "user", "content": prompt}])
                result = llm_client.invoke_structured(KnowledgeChapterProfile, [{"role": "user", "content": prompt}], max_tokens=2000)
                break
            except Exception as e:
                print(f"[build_knowledge] chương {ch_id} attempt {attempt} lỗi: {e}")

        if result is None:
            print(f"[build_knowledge] ❌ chương {ch_id} THẤT BẠI sau 3 lần — dùng profile rỗng")
            knowledge_profile[ch_id] = {"chuong": ch_id, "can_nam": "", "can_hieu": "", "bai_hoc": [], "quan_he_kien_thuc": "", "quan_he_dang_bai": ""}
            failed_chapters.append(ch_id)                          # ← thêm: track lại
        else:
            print(f"[build_knowledge] ✅ chương {ch_id} phân tích thành công")   # ← thêm: log rõ ràng khi OK
            knowledge_profile[ch_id] = result.model_dump()

    return knowledge_profile, failed_chapters


def build_knowledge(state: ExamState, llm_client: LLMClient) -> dict:
    print(" ================================  final build_knowledge  ================================\n"*2)


    if state.get("completed_build_knowlege", False):
        print("build_knowledge xongggggggg")
        return {"current_step": "build_knowledge"}

    messages          = state.get("messages", [])
    knowledge_queue   = state.get("knowledge_queue")
    knowledge_pending = state.get("knowledge_pending")
    knowledge_scores  = state.get("knowledge_scores", {})
    knowledge_retried = state.get("knowledge_retried", False)
    subject           = state.get("student_profile", {}).get("mon_hoc", "")

    if state.get("knowledge_done", False):
        return {}

    if knowledge_queue is None:
        knowledge_queue = _build_queue(state.get("student_profile", {}))

    # ── Xử lý câu trả lời cho lượt hỏi trước (chương thường hoặc retry) ──────
    if knowledge_pending:
        last_input = next((m.content for m in reversed(messages) if isinstance(m, HumanMessage)), "")

        if knowledge_pending.get("type") == "retry":
            missing = knowledge_pending["missing"]
            numbers = re.findall(r'[0-3]', last_input)
            for i, (ch_id, lesson, sec) in enumerate(missing):
                if i < len(numbers):
                    knowledge_scores[ch_id][lesson][sec] = int(numbers[i])
            knowledge_retried = True
        else:
            ch_id = knowledge_pending["chuong"]
            knowledge_scores[ch_id] = _parse_scores_chapter(last_input, subject, ch_id)

    # ── Còn chương chưa hỏi → hỏi tiếp, MỖI CHƯƠNG CHỈ HỎI 1 LẦN ────────────
    if knowledge_queue:
        ch_id        = knowledge_queue[0]
        ch_name      = get_chapter(subject, ch_id)["chapter_name"]
        section_text = _build_chapter_section_text(subject, ch_id)
        template     = KNOWLEDGE_PROMPT_PATH.read_text(encoding="utf-8")
        message_text = template.replace("{chuong}", ch_name).replace("{sections}", section_text)

        return {
            "messages":          [AIMessage(content=message_text)],
            "knowledge_queue":   knowledge_queue[1:],
            "knowledge_pending": {"type": "chapter", "chuong": ch_id},
            "knowledge_scores":  knowledge_scores,
            "knowledge_retried": knowledge_retried,
            "knowledge_done":    False,
            "current_step":      "build_knowledge",
        }

    # ── Đã hỏi hết chương → kiểm tra section thiếu điểm ─────────────────────
    missing = _find_missing_sections(knowledge_scores)

    if missing and not knowledge_retried:
        lines = [f"- [{ch_id}] {lesson} > {sec}" for ch_id, lesson, sec in missing]
        message_text = (
            "Một số chủ đề bạn chưa cho điểm, vui lòng bổ sung theo đúng thứ tự (0-3):\n"
            + "\n".join(lines)
        )
        return {
            "messages":          [AIMessage(content=message_text)],
            "knowledge_pending": {"type": "retry", "missing": missing},
            "knowledge_scores":  knowledge_scores,
            "knowledge_retried": knowledge_retried,
            "knowledge_done":    False,
            "current_step":      "build_knowledge",
        }

    # ── Sau khi hỏi lại (hoặc không có gì thiếu) — section còn thiếu mặc định = 1 ──
    for ch_id, lesson, sec in _find_missing_sections(knowledge_scores):
        knowledge_scores[ch_id][lesson][sec] = 1

    # ── Phase 2: phân tích (LLM DUY NHẤT, 1 lần/chương) ─────────────────────
    knowledge_profile, failed_chapters = _analyze_chapters(
        {**state, "knowledge_scores": knowledge_scores}, llm_client
    )

    warning_msg = ""
    if failed_chapters:
        warning_msg = f"\n⚠️ Lưu ý: {len(failed_chapters)} chương phân tích thất bại (chương {', '.join(failed_chapters)}), đề thi có thể thiếu chiều sâu ở các chương này."

    return {
        "knowledge_scores":         knowledge_scores,
        "knowledge_profile":        knowledge_profile,
        "knowledge_analysis_failed": failed_chapters,   # ← thêm vào state, để evaluate_exam hoặc UI sau này đọc được
        "knowledge_queue":          [],
        "knowledge_pending":        None,
        "knowledge_retried":        knowledge_retried,
        "knowledge_done":           True,
        "current_step":             "build_knowledge",
        "completed_build_knowlege": len(knowledge_profile) > 0,
    }