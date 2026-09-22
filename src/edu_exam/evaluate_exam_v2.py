import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import AIMessage
from src.state_edu import ExamState, ToolSelection, ToolSelectionBatch
from src.clients.llm import LLMClient
from src.edu_qa.tools.math_tools_v2_2 import TOOL_MAP_V2   # ← chỉnh lại path thật của math_tools_v2_2.py trong project
from src.edu_qa.paths import TOOL_SELECT_BATCH_PROMPT_PATH
from typing import Dict, Any

TOOL_VERIFY_BATCH_SIZE = 5




TOOLS_TOP_K            = 3
TOOLS_SCORE_THRESHOLD_1 = 0.6
TOOLS_SCORE_THRESHOLD_2 = 0.4

REQUIRED_FIELDS = [
    "id", "chuong", "bai", "dang_bai", "type", "do_kho",
    "question", "options", "answer", "giai_thich", "y_tuong",
    "chapter_id", "validation_type",
]


# ── Nhiệm vụ 1: kiểm tra schema bằng code ─────────────────────────────────────

def _check_schema(q: dict) -> dict:
    missing = [f for f in REQUIRED_FIELDS if q.get(f) in (None, "", {}, [])]

    options = q.get("options", {})
    for key in ["A", "B", "C", "D"]:
        if not options.get(key):
            missing.append(f"options.{key}")

    if q.get("answer") not in ["A", "B", "C", "D"]:
        missing.append("answer_invalid")

    return {"schema_valid": len(missing) == 0, "missing": missing}


# ── Nhiệm vụ 2: kiểm tra đủ số câu theo yêu cầu/matrix/specs ─────────────────

def _check_counts(state: ExamState) -> dict:
    profile        = state.get("student_profile", {})
    generated_exam = state.get("generated_exam", [])
    question_specs = state.get("question_specs", [])

    expected_total = profile.get("so_cau_hoi", 0)
    actual_total   = len(generated_exam)

    expected_ids = {s["id"] for s in question_specs}
    actual_ids   = {q["id"] for q in generated_exam}
    missing_ids  = sorted(expected_ids - actual_ids)

    return {
        "expected_total": expected_total,
        "actual_total":   actual_total,
        "count_match":    actual_total == expected_total and not missing_ids,
        "missing_spec_ids": missing_ids,
    }


# ── Nhiệm vụ 3: retrieval chọn tool + tính lại cho câu type=bai_tap ──────────
# Tham khảo trực tiếp qa_solve_agent.py — cùng cơ chế rerank + cascade threshold




# ── Nhiệm vụ 3: retrieval chọn tool (per-question) + LLM chọn tool THEO BATCH ──

def _select_candidate_tool_names(retriever, question: str) -> list:
    """Retrieval THUẦN (không LLM) — vẫn chạy riêng từng câu để giữ tool ứng viên sát đúng."""
    docs     = retriever.hybrid_search_tools(question, k=10)
    reranked = retriever.rerank(question, docs, top_k=TOOLS_TOP_K)

    filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_1]
    if not filtered:
        filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_2]
    tools_name  = [d.metadata.get("tool_name") for d in filtered if d.metadata.get("tool_name") in TOOL_MAP_V2]
    print("list tools name : " , tools_name ,"\n\n")
    return tools_name


def _format_questions_block(batch: list, candidate_map: dict) -> str:
    """Câu hỏi 1: ...\ncác tool của câu hỏi 1\n\nCâu hỏi 2: ...\ncác tool của câu hỏi 2..."""
    blocks = []
    for q in batch:
        tool_names = candidate_map.get(q["id"], [])
        if tool_names:
            tool_lines = "\n".join(f"  - {name}: {TOOL_MAP_V2[name].description}" for name in tool_names)
        else:
            tool_lines = "  (không có tool nào khớp)"
        blocks.append(f"Câu hỏi {q['id']}: {q['question']}\nCác tool khả dụng cho câu hỏi này:\n{tool_lines}")
    return "\n\n".join(blocks)


def _check_mapping(tool_output: str, chosen_option_text: str) -> bool:
    """So khớp thô giữa kết quả tool và nội dung đáp án LLM đã chọn — substring 2 chiều, bỏ khoảng trắng/hoa-thường."""
    if not tool_output or not chosen_option_text:
        return False
    a = str(tool_output).strip().lower()
    b = str(chosen_option_text).strip().lower()
    return b in a or a in b


def _verify_bai_tap_with_tools(generated_exam: list, retriever, llm_client: LLMClient) -> None:
    bai_tap_questions = [q for q in generated_exam if q.get("type") == "bai_tap"]
    if not bai_tap_questions:
        return

    template = TOOL_SELECT_BATCH_PROMPT_PATH.read_text(encoding="utf-8")

    for i in range(0, len(bai_tap_questions), TOOL_VERIFY_BATCH_SIZE):
        batch = bai_tap_questions[i:i + TOOL_VERIFY_BATCH_SIZE]

        # Retrieval riêng từng câu (không LLM) — rẻ, giữ tool ứng viên sát đúng theo từng câu
        candidate_map = {q["id"]: _select_candidate_tool_names(retriever, q["question"]) for q in batch}

        if not any(candidate_map.values()):
            for q in batch:
                q["tool_used"], q["answer_tools"], q["mapping"] = None, "Không tìm được tool phù hợp", "❌"
            continue

        prompt = template.replace("{questions_block}", _format_questions_block(batch, candidate_map))

        print(" ====================== prompt chọn tools ======================\n   \n")
        print(prompt)

        result = llm_client.invoke_structured(ToolSelectionBatch, [{"role": "user", "content": prompt}], max_tokens=2000)
        selections_by_id = {s.id: s for s in result.selections} if result else {}

        for q in batch:
            sel = selections_by_id.get(q["id"])
            if not sel or sel.tool_name not in TOOL_MAP_V2:
                q["tool_used"], q["answer_tools"], q["mapping"] = None, "LLM không chọn được tool hợp lệ", "❌"
                continue

            try:
                output = TOOL_MAP_V2[sel.tool_name].invoke(sel.tool_args)
            except Exception as e:
                output = f"LOI: {e}"

            q["tool_used"]    = sel.tool_name
            q["answer_tools"] = output

            print(f" >>> Câu {q['id']} tool {sel.tool_name} output: {output}")

            if isinstance(output, str) and output.startswith("LOI:"):
                q["mapping"] = "❌"
            else:
                chosen_text = q.get("options", {}).get(q.get("answer", ""), "")
                q["mapping"] = "✅" if _check_mapping(output, chosen_text) else "❌"


# ── Node chính ─────────────────────────────────────────────────────────────────
MAX_RETRY = 2   # tối đa 2 lần quay lại sinh bù, tránh loop vô hạn nếu LLM cứ lỗi mãi


def evaluate_exam(state: ExamState, llm_client: LLMClient, retriever) -> dict:
    print(" ------------------------------ file evaluate_exam ------------------------------\n"*2)

    if state.get("evaluate_done", False):
        return {}

    generated_exam = state.get("generated_exam", [])
    retry_count    = state.get("evaluate_retry_count", 0)

    print("\n----------\n xem các câu bài tập và kết quả tool tính lại:")
    for q in generated_exam:
        if q.get("type") == "bai_tap":
            print(f"id={q['id']} | tool={q.get('tool_used')} | answer_tools={q.get('answer_tools')} | "
                f"answer_LLM={q.get('answer')}={q['options'].get(q.get('answer'))} | mapping={q.get('mapping')}")

    # 1. Schema check
    for q in generated_exam:
        result = _check_schema(q)
        q["schema_check"]    = result
        q["need_regenerate"] = not result["schema_valid"]

    # 2. Count check
    count_result = _check_counts(state)

    invalid_ids    = {q["id"] for q in generated_exam if q["need_regenerate"]}
    missing_ids    = set(count_result["missing_spec_ids"])
    regenerate_ids = invalid_ids | missing_ids

    # ── Còn câu cần sinh lại và chưa hết lượt retry → quay lại generate_questions ──
    if regenerate_ids and retry_count < MAX_RETRY:
        print(f">>> evaluate_exam: {len(regenerate_ids)} câu cần sinh lại (retry {retry_count + 1}/{MAX_RETRY}): {sorted(regenerate_ids)}")
        cleaned_exam = [q for q in generated_exam if q["id"] not in regenerate_ids]   # loại câu lỗi, giữ lại câu tốt

        return {
            "generated_exam":       cleaned_exam,
            "regenerate_ids":       sorted(regenerate_ids),
            "evaluate_retry_count": retry_count + 1,
            "generate_done":        False,   # ← cho graph quay lại generate_questions
            "evaluate_done":        False,
            "current_step":         "evaluate_exam",
        }

    # ── Không còn gì cần sinh lại (hoặc hết lượt retry) → tool verify + kết thúc ──
    if regenerate_ids:
        print(f">>> evaluate_exam: hết {MAX_RETRY} lượt retry, còn {len(regenerate_ids)} câu lỗi, vẫn tiếp tục với đề hiện có")

    _verify_bai_tap_with_tools(generated_exam, retriever, llm_client)

    n_invalid    = len(regenerate_ids)
    n_bai_tap    = sum(1 for q in generated_exam if q.get("type") == "bai_tap")
    n_mapping_ok = sum(1 for q in generated_exam if q.get("mapping") == "✅")

    summary = (
        f"✅ Kiểm tra hoàn tất.\n"
        f"- Schema: {len(generated_exam) - n_invalid}/{len(generated_exam)} câu đạt chuẩn"
        f" ({n_invalid} câu còn lỗi sau {retry_count} lần retry)\n"
        f"- Số câu: {'ĐỦ' if count_result['count_match'] else 'THIẾU'}"
        f" ({count_result['actual_total']}/{count_result['expected_total']})\n"
        f"- Đối chiếu tool: {n_mapping_ok}/{n_bai_tap} câu bài_tập khớp kết quả tool tính lại"
    )
    print(summary)

    return {
        "messages":       [AIMessage(content=summary)],
        "generated_exam": generated_exam,
        "count_check":    count_result,
        "evaluate_done":  True,
        "current_step":   "evaluate_exam",
    }