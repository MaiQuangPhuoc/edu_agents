import sys, os, re , json 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import AIMessage
# from src.state_edu import ExamState, ToolSelection, ToolSelectionBatch
from src.state_edu import ExamState

from src.clients.llm import LLMClient
# from src.edu_qa.tools.math_tools_v2_2 import TOOL_MAP_V2   # ← chỉnh lại path thật của math_tools_v2_2.py trong project
from src.edu_qa.paths import TEST_EXAM_PROMPT_PATH
from typing import Dict, Any
TOOL_VERIFY_BATCH_SIZE = 5




# TOOLS_TOP_K            = 4
# TOOLS_SCORE_THRESHOLD_1 = 0.5
# TOOLS_SCORE_THRESHOLD_2 = 0.3

# NO_TOOL_NAME = "khong_co_tool_phu_hop"   # phải trùng với chuỗi trong schema ToolSelection và prompt


# def _norm_chapter(s: str) -> str:
#     s = (s or "").lower().strip()
#     s = re.sub(r"^chương\s*[ivx\d]+\s*[:\-–.]?\s*", "", s)
#     return re.sub(r"\s+", " ", s)


# def _chapter_match(a: str, b: str) -> bool:
#     a, b = _norm_chapter(a), _norm_chapter(b)
#     return bool(a and b and (a == b or a in b or b in a))



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

# def _select_candidate_tool_names(retriever, q: dict) -> list:
#     """Lọc cứng theo chương rồi đưa toàn bộ tool của chương cho LLM chọn (chương chỉ có 3-7 tool)."""
#     query = f"{q.get('dang_bai', '')}: {q['question']}"
#     print("="*30)

#     print(f"query : {query}")
#     print("="*30)

#     docs  = retriever.hybrid_search_tools(query, k=15)   # collection tools nhỏ nên k=50 lấy hết

#     ch_docs = [d for d in docs if _chapter_match(d.metadata.get("chapter_name", ""), q.get("chuong", ""))]

#     # ── Dự phòng: chương không khớp thì rerank top-K trên toàn bộ kết quả ──
#     if not ch_docs:
#         print(f"  ⚠ không khớp chương '{q.get('chuong')}', dùng rerank top-{TOOLS_TOP_K}")
#         ch_docs = retriever.rerank(query, docs, top_k=TOOLS_TOP_K)

#     # ── Rerank + ngưỡng trong chương (ĐANG TẮT, cần thì mở 6 dòng dưới) ──
#     # reranked = retriever.rerank(query, ch_docs, top_k=TOOLS_TOP_K)
#     # filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_1]
#     # if not filtered:
#     #     filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_2]
#     # ch_docs = filtered

#     tools_name = list(dict.fromkeys(   # khử trùng, giữ thứ tự
#         d.metadata.get("tool_name") for d in ch_docs if d.metadata.get("tool_name") in TOOL_MAP_V2
#     ))
#     print("="*30)
#     print("list tools name : ", tools_name, "\n\n")
#     print("="*30)

#     return tools_name


# def _format_questions_block(batch: list, candidate_map: dict) -> str:
#     """Câu hỏi 1: ...\ncác tool của câu hỏi 1\n\nCâu hỏi 2: ...\ncác tool của câu hỏi 2..."""
#     blocks = []
#     for q in batch:
#         tool_names = candidate_map.get(q["id"], [])
#         if tool_names:
#             tool_lines = "\n".join(f"  - {name}: {TOOL_MAP_V2[name].description}" for name in tool_names)
#         else:
#             tool_lines = f"  (không có tool nào khớp, trả tool_name = {NO_TOOL_NAME})"
#         blocks.append(f"Câu hỏi {q['id']}: {q['question']}\nCác tool khả dụng cho câu hỏi này:\n{tool_lines}")

#     print("=" * 80)
#     print(blocks)
#     print("=" * 80)
#     return "\n\n".join(blocks)


# def _check_mapping(tool_output: str, chosen_option_text: str) -> bool:
#     """So khớp thô giữa kết quả tool và nội dung đáp án LLM đã chọn — substring 2 chiều, bỏ khoảng trắng/hoa-thường."""
#     if not tool_output or not chosen_option_text:
#         return False
#     a = str(tool_output).strip().lower()
#     b = str(chosen_option_text).strip().lower()
#     return b in a or a in b

import builtins, io, contextlib, textwrap, warnings
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import List
from pydantic import BaseModel, Field
warnings.filterwarnings("ignore", category=SyntaxWarning)

CODE_VERIFY_BATCH_SIZE = 4
MAX_FIX_RETRY = 2

_PRELUDE = "from sympy import *\nx, y, z, t, m, n, k = symbols('x y z t m n k')\n"
_BLOCKED_NAMES = {"open", "compile", "input", "help", "exit", "quit"}


def _safe_import(name, *args, **kwargs):
    allowed_roots = {"sympy", "math", "itertools", "fractions", "decimal", "collections", "re"}
    if name.split(".")[0] not in allowed_roots:
        raise ImportError(f"Không được phép import '{name}' trong sandbox")
    return builtins.__import__(name, *args, **kwargs)


def run_sympy_code(code: str, timeout: int = 15):
    def _run():
        buf = io.StringIO()
        try:
            safe_builtins = {k: v for k, v in vars(builtins).items() if k not in _BLOCKED_NAMES}
            safe_builtins["__import__"] = _safe_import
            ns = {"__builtins__": safe_builtins}
            exec(_PRELUDE, ns)
            clean_code = textwrap.dedent(code).strip()
            with contextlib.redirect_stdout(buf):
                exec(clean_code, ns)
            return "ok", buf.getvalue()
        except Exception as e:
            return "err", f"{type(e).__name__}: {e}"

    with ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(_run)
        try:
            return future.result(timeout=timeout)
        except FutureTimeoutError:
            return "timeout", ""


class CodeSolution(BaseModel):
    id: int = Field(description="id câu hỏi, khớp id đã cho")
    code: str = Field(description="Code Python dùng sympy, PHẢI print() giá trị trung gian trước khi kết luận, cuối cùng in đúng 1 dòng ANSWER: A|B|C|D, hoặc ANSWER: NONE nếu không giải được bằng code")

class CodeSolutionBatch(BaseModel):
    solutions: List[CodeSolution]

CODE_PROMPT_TEMPLATE = """Bạn kiểm tra đáp án bài tập Toán 10 bằng code sympy.

Với MỖI câu, viết code Python:
1. Tự tính kết quả từ dữ kiện đề bài bằng phép tính thật (KHÔNG suy luận bằng lời rồi gán thẳng đáp án).
2. BẮT BUỘC print() từng giá trị trung gian trước khi kết luận.
3. So sánh bằng GIÁ TRỊ SỐ/TOÁN HỌC, không so chuỗi text nguyên văn của option:
   - Nếu option chứa số/tọa độ/biểu thức: dùng regex hoặc sympy.sympify để tách số ra từ chuỗi option,
     rồi so bằng dấu == hoặc sympy.simplify(a - b) == 0.
   - Nếu option là tọa độ/cặp giá trị (x, y): so từng thành phần riêng, KHÔNG trừ trực tiếp 2 tuple,
     KHÔNG so chuỗi text có bọc chữ như "I(...)" hay "Đỉnh...".
   - Nếu option là tập hợp: parse thành set/FiniteSet rồi so bằng ==, không so chuỗi.
   - Nếu option là khoảng nghiệm: dựng lại Interval/Union từ option rồi so == hoặc .equals(),
     KHÔNG tự đặt biến boolean diễn giải bằng lời rồi bỏ trống.
   - Khi so 2 giá trị số, LUÔN ép về float trước khi so: abs(float(a) - float(b)) < 1e-6,
     KHÔNG dùng == trực tiếp giữa Rational và Float.
4. Gán is_A, is_B, is_C, is_D từ kết quả so sánh giá trị ở bước 3.
5. Dòng cuối: ans = "A" if is_A else "B" if is_B else "C" if is_C else "D" if is_D else "NONE"
   print("ANSWER:", ans)
6. Với bài toán đơn giản, ưu tiên tự suy luận đại số trực tiếp thay vì gọi hàm giải bất phương trình phức tạp.
7. Khai báo đầy đủ MỌI biến trước khi dùng.
8. Nếu option có NHIỀU điều kiện gộp lại (số + kết luận định tính như "vuông góc", "cùng phương"...),
   phải kiểm tra ĐỦ TẤT CẢ các phần đều đúng thì is_X mới True.

Đã có sẵn: from sympy import *, biến x,y,z,t,m,n,k. Không import thêm ngoài re nếu cần.
Với tập hợp dùng set/FiniteSet. Câu nhiều ý thì mọi ý phải khớp trong cùng 1 option.

{questions_block}
"""

FIX_PROMPT_TEMPLATE = """Bạn kiểm tra và sửa lại code Python/sympy đã viết trước đó cho các câu bài tập Toán 10.

Với MỖI câu bên dưới, code cũ đã chạy nhưng gặp lỗi hoặc chưa kết luận được. Hãy sửa lại đúng lỗi, giữ nguyên các quy tắc:
- BẮT BUỘC print() từng giá trị trung gian trước khi kết luận.
- So sánh bằng GIÁ TRỊ SỐ/TOÁN HỌC, không so chuỗi text nguyên văn của option.
- Nếu option là tọa độ/cặp giá trị: so từng thành phần riêng, KHÔNG trừ trực tiếp 2 tuple.
- Nếu option là tập hợp: parse thành set/FiniteSet rồi so bằng ==.
- Nếu option là khoảng nghiệm: dựng lại Interval/Union rồi so == hoặc .equals().
- Dòng cuối: ans = "A" if is_A else "B" if is_B else "C" if is_C else "D" if is_D else "NONE"
  print("ANSWER:", ans)
- Khai báo đầy đủ mọi biến trước khi dùng.

Đã có sẵn: from sympy import *, biến x,y,z,t,m,n,k. Không import thêm ngoài re nếu cần.

{questions_block}
"""


def _format_code_block(batch: list) -> str:
    blocks = []
    for q in batch:
        opts = "\n".join(f"  {k}. {v}" for k, v in q.get("options", {}).items())
        blocks.append(f"Câu hỏi {q['id']}: {q['question']}\n{opts}")
    return "\n\n".join(blocks)


def _format_fix_block(batch: list, prev_code: dict, prev_error: dict) -> str:
    blocks = []
    for q in batch:
        opts = "\n".join(f"  {k}. {v}" for k, v in q.get("options", {}).items())
        blocks.append(
            f"Câu hỏi {q['id']}: {q['question']}\n{opts}\n\n"
            f"Code đã viết trước đó:\n{prev_code.get(q['id'], '')}\n\n"
            f"Kết quả chạy: {prev_error.get(q['id'], '')}"
        )
    return "\n\n".join(blocks)


def _run_code_once(batch: list, prompt: str, llm_client: LLMClient) -> dict:
    result = llm_client.invoke_structured(CodeSolutionBatch, [{"role": "user", "content": prompt}],
                                           max_tokens=min(1200 * len(batch), 8000))
    by_id = {s.id: s for s in result.solutions} if result else {}

    out = {}
    for q in batch:
        sol = by_id.get(q["id"])
        if not sol:
            out[q["id"]] = {"code": "", "status": "no_response", "answer": None, "error": "LLM không trả code cho câu này"}
            continue
        status, raw = run_sympy_code(sol.code)
        m = re.search(r"ANSWER:\s*([ABCD]|NONE)", raw or "")
        if status != "ok":
            out[q["id"]] = {"code": sol.code, "status": status, "answer": None, "error": raw or status}
        elif not m or m.group(1) == "NONE":
            out[q["id"]] = {"code": sol.code, "status": "no_answer", "answer": None,
                             "error": f"Code chạy được nhưng không kết luận được option (output: {raw.strip()[:300]})"}
        else:
            out[q["id"]] = {"code": sol.code, "status": "ok", "answer": m.group(1), "error": ""}
    return out



def _verify_bai_tap_with_code(generated_exam: list, llm_client: LLMClient) -> None:
    bai_tap_questions = [q for q in generated_exam if q.get("type") == "bai_tap"]
    if not bai_tap_questions:
        return

    for i in range(0, len(bai_tap_questions), CODE_VERIFY_BATCH_SIZE):
        batch = bai_tap_questions[i:i + CODE_VERIFY_BATCH_SIZE]

        prompt = CODE_PROMPT_TEMPLATE.replace("{questions_block}", _format_code_block(batch))
        state = _run_code_once(batch, prompt, llm_client)

        for attempt in range(MAX_FIX_RETRY):
            need_fix = [q for q in batch if state[q["id"]]["answer"] is None]
            if not need_fix:
                break
            print(f"  [retry {attempt + 1}/{MAX_FIX_RETRY}] {len(need_fix)} câu cần sửa: {[q['id'] for q in need_fix]}")
            prev_code  = {q["id"]: state[q["id"]]["code"] for q in need_fix}
            prev_error = {q["id"]: state[q["id"]]["error"] for q in need_fix}
            fix_prompt = FIX_PROMPT_TEMPLATE.replace("{questions_block}", _format_fix_block(need_fix, prev_code, prev_error))
            state.update(_run_code_once(need_fix, fix_prompt, llm_client))

        for q in batch:
            s = state[q["id"]]
            q["tool_used"] = "code"
            if s["answer"] is None:
                q["answer_tools"], q["check"] = "", "N/A"
            else:
                q["answer_tools"] = s["answer"]
                q["check"] = "✅" if s["answer"] == q.get("answer") else "❌"

# thêm 2 trường answer-tools và check vào json đề kiểm tra 
def _update_exam_json_with_tool_check(generated_exam: list) -> None:
    """Lấy file exam_*.json mới nhất trong TEST_EXAM_PROMPT_PATH, ghi answer_tools + check theo id."""
    print(f"---------------------- hàm thêm 2 trường check và answer_tools --------------------- \n")
    files = sorted(TEST_EXAM_PROMPT_PATH.glob("exam_*.json"))
    if not files:
        print("  ⚠ không tìm thấy file exam_*.json để cập nhật")
        return

    path = files[-1]
    by_id = {q["id"]: q for q in generated_exam}

    exam_on_disk = json.loads(path.read_text(encoding="utf-8"))
    updated = 0
    for q in exam_on_disk:
        src = by_id.get(q.get("id"))
        if src is None:
            continue
        q["answer_tools"] = src.get("answer_tools", "")
        q["check"]        = src.get("check", "")
        updated += 1

    path.write_text(json.dumps(exam_on_disk, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">>> đã cập nhật {updated}/{len(exam_on_disk)} câu vào {path.name}")

# ── Node chính ─────────────────────────────────────────────────────────────────
MAX_RETRY = 2   # tối đa 2 lần quay lại sinh bù, tránh loop vô hạn nếu LLM cứ lỗi mãi


def evaluate_exam(state: ExamState, llm_client: LLMClient) -> dict:
    print(" ------------------------------ file evaluate_exam ------------------------------\n"*2)



    if state.get("evaluate_done", False):
        return {}

    generated_exam = state.get("generated_exam", [])
    retry_count    = state.get("evaluate_retry_count", 0)

    # print("\n----------\n xem các câu bài tập và kết quả tool tính lại:")
    # for q in generated_exam:
    #     if q.get("type") == "bai_tap":
    #         print(f"id={q['id']} | tool={q.get('tool_used')} | answer_tools={q.get('answer_tools')} | "
    #             f"answer_LLM={q.get('answer')}={q['options'].get(q.get('answer'))} | check={q.get('check')}")

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

    _verify_bai_tap_with_code(generated_exam, llm_client)
    _update_exam_json_with_tool_check(generated_exam)

    n_invalid    = len(regenerate_ids)
    n_bai_tap    = sum(1 for q in generated_exam if q.get("type") == "bai_tap")
    n_ok    = sum(1 for q in generated_exam if q.get("check") == "✅")
    n_wrong = sum(1 for q in generated_exam if q.get("check") == "❌")
    n_na    = sum(1 for q in generated_exam if q.get("check") == "N/A")

    summary = (
        f"✅ Kiểm tra hoàn tất.\n"
        f"- Schema: {len(generated_exam) - n_invalid}/{len(generated_exam)} câu đạt chuẩn"
        f" ({n_invalid} câu còn lỗi sau {retry_count} lần retry)\n"
        f"- Số câu: {'ĐỦ' if count_result['count_match'] else 'THIẾU'}"
        f" ({count_result['actual_total']}/{count_result['expected_total']})\n"
        f"- Đối chiếu tool ({n_bai_tap} câu bài_tập): khớp {n_ok} | sai {n_wrong}"
    )
    print(summary)

    return {
        "messages":       [AIMessage(content=summary)],
        "generated_exam": generated_exam,
        "count_check":    count_result,
        "evaluate_done":  True,
        "current_step":   "evaluate_exam",
    }