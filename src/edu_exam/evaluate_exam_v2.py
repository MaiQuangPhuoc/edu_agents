import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import AIMessage
from src.state_edu import ExamState
from src.clients.llm import LLMClient
from src.edu_qa.tools.math_tools_v2_2 import TOOL_MAP_V2   # ← chỉnh lại path thật của math_tools_v2_2.py trong project

TOOL_SELECT_PROMPT_PATH = Path(r'D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\prompt_edu\prompt\qa_solve_tool_select_prompt.txt')

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

def _select_candidate_tools(retriever, query: str) -> list:
    docs     = retriever.hybrid_search_tools(query, k=10)
    reranked = retriever.rerank(query, docs, top_k=TOOLS_TOP_K)

    filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_1]
    if not filtered:
        filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_2]

    tool_names = [d.metadata.get("tool_name") for d in filtered]
    return [TOOL_MAP_V2[name] for name in tool_names if name in TOOL_MAP_V2]


def _select_and_call_tool(question: str, retriever, llm_client: LLMClient):
    """Trả về (tool_name, tool_output) — output=None nếu không tool nào phù hợp/tính lỗi."""
    candidate_tools = _select_candidate_tools(retriever, question)
    if not candidate_tools:
        return None, None

    template    = TOOL_SELECT_PROMPT_PATH.read_text(encoding="utf-8")
    prompt_text = template.format(question=question)

    llm_with_tools = llm_client._llm.bind_tools(candidate_tools)
    response = llm_with_tools.invoke([{"role": "user", "content": prompt_text}])

    if not response.tool_calls:
        return None, None

    tool_call = response.tool_calls[0]
    tool_fn   = TOOL_MAP_V2.get(tool_call["name"])
    if not tool_fn:
        return tool_call["name"], None

    try:
        output = tool_fn.invoke(tool_call["args"])
    except Exception as e:
        print(f"[tool_error] {tool_call['name']}: {e}")
        return tool_call["name"], None

    if isinstance(output, str) and output.startswith("LOI:"):
        return tool_call["name"], None

    return tool_call["name"], output


def _check_mapping(tool_output: str, chosen_option_text: str) -> bool:
    """So khớp thô giữa kết quả tool và nội dung đáp án LLM đã chọn — substring 2 chiều, bỏ khoảng trắng/hoa-thường."""
    if not tool_output or not chosen_option_text:
        return False
    a = str(tool_output).strip().lower()
    b = str(chosen_option_text).strip().lower()
    return b in a or a in b


def _verify_bai_tap_with_tools(generated_exam: list, retriever, llm_client: LLMClient) -> None:
    for q in generated_exam:
        if q.get("type") != "bai_tap":
            continue

        tool_name, tool_output = _select_and_call_tool(q.get("question", ""), retriever, llm_client)

        q["tool_used"]    = tool_name
        q["answer_tools"] = tool_output if tool_output is not None else "Không tìm được tool phù hợp / tính lỗi"

        chosen_text = q.get("options", {}).get(q.get("answer", ""), "")
        matched = _check_mapping(tool_output, chosen_text) if tool_output is not None else False
        q["mapping"] = "✅" if matched else "❌"


# ── Node chính ─────────────────────────────────────────────────────────────────
MAX_RETRY = 2   # tối đa 2 lần quay lại sinh bù, tránh loop vô hạn nếu LLM cứ lỗi mãi


def evaluate_exam(state: ExamState, llm_client: LLMClient, retriever) -> dict:
    print(">>> [Node] evaluate_exam")

    if state.get("evaluate_done", False):
        return {}

    generated_exam = state.get("generated_exam", [])
    retry_count    = state.get("evaluate_retry_count", 0)

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