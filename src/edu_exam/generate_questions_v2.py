import json
import sys, os

from click import prompt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import datetime
from pathlib import Path
from langchain_core.messages import AIMessage
from src.state_edu import ExamState, GeneratedQuestionBatch, GeneratedQuestion
from src.clients.llm import LLMClient
from src.edu_exam.curriculum import get_chapter
from src.edu_qa.paths import GENERATE_QUESTIONS_PROMPT_PATH , TEST_EXAM_PROMPT_PATH

PROMPT_PATH = GENERATE_QUESTIONS_PROMPT_PATH
OUTPUT_DIR  = TEST_EXAM_PROMPT_PATH
BATCH_SIZE  = 5


def _save_exam_json(generated_exam: list) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path  = OUTPUT_DIR / f"exam_{timestamp}.json"

    exam_clean = [
        {
            "chuong":     q.get("chuong", ""),
            "bai":        q.get("bai", ""),
            "dang_bai":   q.get("dang_bai", ""),
            "type":       q.get("type", ""),
            "do_kho":     q.get("do_kho", ""),
            "question":   q.get("question", ""),
            "options":    q.get("options", {}),
            "answer":     q.get("answer", ""),
            "giai_thich": q.get("giai_thich", ""),
        }
        for q in generated_exam
    ]

    out_path.write_text(json.dumps(exam_clean, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">>> Đã lưu đề thi: {out_path}")
    return out_path


def _get_chunks_for_batch(retrieved_chunks: list, ch_id: str, bai_names: set) -> str:
    """Lọc chunk theo 'bai' (spec) khớp 'lesson' (metadata chunk) — match chính xác bằng code."""
    bai_lower = {b.lower() for b in bai_names if b}
    matched = [
        c["content"]
        for c in retrieved_chunks
        if c["metadata"].get("chapter_id", "") == ch_id
        and any(b in c["metadata"].get("lesson", "").lower() or c["metadata"].get("lesson", "").lower() in b for b in bai_lower)
    ]
    print(f"[{ch_id}] bai_names={bai_lower} → {len(matched)} chunk khớp lesson")   # ← thêm dòng này
    return "\n---\n".join(matched)


def _format_lesson_reference(subject: str, ch_id: str) -> str:
    """Danh sách bài học hợp lệ trong chương — cho LLM tham khảo để bám đúng phạm vi, không tự bịa bài học."""
    lessons = get_chapter(subject, ch_id)["lessons"].keys()
    return "\n".join(f"- {l}" for l in lessons)


def _format_specs(specs: list) -> str:
    lines = []
    for s in specs:
        lines.append(
            f"id={s['id']} | dang_bai={s['dang_bai']} | do_kho_du_kien={s['do_kho']} | "
            f"yeu_cau={s['yeu_cau']} | ngu_canh={', '.join(s.get('ngu_canh', []))}"
        )
    return "\n".join(lines)


def _format_memory(exam_memory: list) -> str:
    if not exam_memory:
        return "Chưa có câu nào."
    return "\n".join(f"- id={m['id']} | dang_bai={m['dang_bai']} | y_tuong={m['y_tuong']}" for m in exam_memory[-20:])


def _check_duplicate_options(options: dict) -> bool:
    """True nếu có ít nhất 2 đáp án trùng nội dung (chuẩn hóa khoảng trắng/hoa-thường trước khi so)."""
    values = [str(v).strip().lower() for v in options.values()]
    return len(values) != len(set(values))


def generate_questions(state: ExamState, llm_client: LLMClient) -> dict:
    print(">>> [Node] generate_questions")

    if state.get("generate_done", False):
        return {}

    question_specs   = state.get("question_specs", [])
    regenerate_ids   = state.get("regenerate_ids")       # ← thêm: None lần đầu, list id ở các lần quay lại
    retrieved_chunks = state.get("retrieved_chunks", [])
    exam_memory      = state.get("exam_memory", [])
    generated_exam   = state.get("generated_exam", [])   # ← đã là "cleaned_exam" (câu tốt) nếu đang ở chế độ regenerate
    subject          = state.get("student_profile", {}).get("mon_hoc", "")

    if regenerate_ids:
        specs_to_process = [s for s in question_specs if s["id"] in set(regenerate_ids)]
        print(f">>> generate_questions: CHẾ ĐỘ REGENERATE — {len(specs_to_process)} câu cần sinh lại: {regenerate_ids}")
    else:
        specs_to_process = question_specs

    template       = PROMPT_PATH.read_text(encoding="utf-8")
    # structured_llm = llm_client._llm.with_structured_output(GeneratedQuestionBatch)

    specs_by_chapter = {}
    for s in specs_to_process:
        specs_by_chapter.setdefault(s.get("chapter_id", ""), []).append(s)

    for ch_id, ch_specs in specs_by_chapter.items():
        print(f"\n[{ch_id}] bắt đầu sinh {len(ch_specs)} câu")
        ch_raw     = ch_specs[0].get("chuong", "")
        lesson_ref = _format_lesson_reference(subject, ch_id)

        n_docs_chapter = len([c for c in retrieved_chunks if c["metadata"].get("chapter_id", "") == ch_id])   # ← thêm
        print(f"[{ch_id}] tổng chunk retrieve được cho cả chương: {n_docs_chapter}")                          # ← thêm

        for i in range(0, len(ch_specs), BATCH_SIZE):
            batch_specs = ch_specs[i:i + BATCH_SIZE]
            batch_idx   = i // BATCH_SIZE

            bai_names_batch = {s.get("bai", "") for s in batch_specs}          # ← lấy 'bai' thay vì 'dang_bai'
            chunks_batch    = _get_chunks_for_batch(retrieved_chunks, ch_id, bai_names_batch)   # ← hàm mới

            prompt = (template
                      .replace("{chuong}", ch_raw)
                      .replace("{danh_sach_bai_hoc_chuong}", lesson_ref)
                      .replace("{question_specs}", _format_specs(batch_specs))
                      .replace("{chunks}", chunks_batch)
                      .replace("{exam_memory}", _format_memory(exam_memory))
                      .replace("{so_cau}", str(len(batch_specs))))

            specs_by_id     = {s["id"]: s for s in batch_specs}
            questions_batch: list[GeneratedQuestion] = []

            for attempt in range(3):
                try:
                    # result: GeneratedQuestionBatch = structured_llm.invoke([{"role": "user", "content": prompt}])
                    # result = llm_client.invoke_structured(GeneratedQuestionBatch, [{"role": "user", "content": prompt}], max_tokens=8000)
                    result = llm_client.invoke_structured(
                        GeneratedQuestionBatch, [{"role": "user", "content": prompt}],
                        max_tokens=min(1500 * len(batch_specs), 16000),
                    )
                    if len(result.questions) == len(batch_specs):
                        questions_batch = result.questions
                        break
                    print(f"[{ch_id}] batch {batch_idx} attempt {attempt}: {len(result.questions)}/{len(batch_specs)}, retry")
                except Exception as e:
                    print(f"[{ch_id}] batch {batch_idx} attempt {attempt} lỗi: {e}")

            for gq in questions_batch:
                spec = specs_by_id.get(gq.id)
                if not spec:
                    print(f"[{ch_id}] cảnh báo: id={gq.id} không khớp spec nào trong batch, bỏ qua")
                    continue

                q = gq.model_dump()
                q["chuong"]          = ch_raw
                q["bai"]             = spec.get("bai", "")
                q["dang_bai"]        = spec.get("dang_bai", "")
                q["chapter_id"]      = ch_id
                q["validation_type"] = spec.get("validation_type", "llm_review")   # giữ nguyên từ build_specs, chưa đụng evaluate_exam

                errors = []
                if _check_duplicate_options(q["options"]):
                    errors.append("Đáp án bị trùng nội dung")
                q["validation"] = {"hard_check": "pass" if not errors else "fail", "errors": errors}

                generated_exam.append(q)
                exam_memory.append({
                    "id": q["id"], "chuong": ch_raw, "bai": q["bai"],
                    "dang_bai": q["dang_bai"], "y_tuong": q["y_tuong"],
                })

        print(f"[{ch_id}] hoàn tất — tổng: {len(generated_exam)} câu")

    exam_json = json.dumps(generated_exam, ensure_ascii=False, indent=2)
    _save_exam_json(generated_exam)

    print(f"\n>>> generate_questions hoàn tất: {len(generated_exam)} câu")

    return {
        "messages":       [AIMessage(content=exam_json)],
        "generated_exam": generated_exam,
        "exam_memory":    exam_memory,
        "regenerate_ids": [],   # ← reset, evaluate_exam sẽ set lại nếu vòng sau vẫn còn lỗi
        "generate_done":  True,
        "current_step":   "generate_questions",
    }