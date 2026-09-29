import sys, os, re, json, builtins, io, contextlib, warnings ,  textwrap
import multiprocessing as mp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from src.configs import env_config
from src.clients.llm import LLMClient
from src.state_edu import ToolSelectionBatch
warnings.filterwarnings("ignore", category=SyntaxWarning)
# ── ĐƯỜNG DẪN FILE 10 CÂU — thay bằng path thật của bạn ──
QUESTIONS_MD_PATH = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\test_exam\list_10_2.md")

BATCH_SIZE = 4   # đổi 1, 2, 3, 5... tùy lúc chạy
MAX_FIX_RETRY = 2

# ═════════════════════ Parse file .md thành list câu hỏi ═════════════════════

def _parse_questions_md(path: Path) -> list:
    raw_blocks = path.read_text(encoding="utf-8").split("---")
    questions = []
    for i, block in enumerate(raw_blocks, start=1):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        q_lines, options, answer = [], {}, ""
        for line in lines:
            m_opt = re.match(r'^([ABCD])[\.\)]\s*(.+)$', line.strip())
            m_ans = re.match(r'^(đáp án|answer)\s*[:\-]\s*([ABCD])', line.strip(), re.IGNORECASE)
            if m_opt:
                options[m_opt.group(1)] = m_opt.group(2).strip()
            elif m_ans:
                answer = m_ans.group(2).upper()
            else:
                q_lines.append(line.strip())
        questions.append({
            "id": i, "question": "\n".join(q_lines), "options": options, "answer": answer,
            "chuong": "", "dang_bai": "", "type": "bai_tap",
        })
    return questions


# ═════════════════════ Sandbox chạy code sympy ═════════════════════


_PRELUDE = "from sympy import *\nx, y, z, t, m, n, k = symbols('x y z t m n k')\n"


_BLOCKED_NAMES = {"open",   "compile", "input", "help", "exit", "quit"}


def _safe_import(name, *args, **kwargs):
    allowed_roots = {"sympy", "math", "itertools", "fractions", "decimal", "collections", "re"}
    root = name.split(".")[0]
    if root not in allowed_roots:
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
            clean_code = textwrap.dedent(code).strip()   # ← thêm dòng này
            with contextlib.redirect_stdout(buf):
                exec(clean_code, ns)                     # ← đổi code thành clean_code
            return "ok", buf.getvalue()
        except Exception as e:
            return "err", f"{type(e).__name__}: {e}"

    with ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(_run)
        try:
            return future.result(timeout=timeout)
        except FutureTimeoutError:
            return "timeout", ""
        

# ═════════════════════ Schema + prompt cho hướng CODE ═════════════════════

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
   - Nếu option chứa số/tọa độ/biểu thức: tách số ra từ chuỗi option rồi so bằng == hoặc sympy.simplify(a-b)==0.
   - Nếu option là tọa độ/cặp giá trị (x, y): so từng thành phần riêng, KHÔNG trừ trực tiếp 2 tuple,
     KHÔNG so chuỗi text có bọc chữ như "I(...)" hay "Đỉnh...".
   - Nếu option là tập hợp: parse thành set/FiniteSet rồi so bằng ==, không so chuỗi.
   - Nếu option là khoảng nghiệm: dựng lại Interval/Union từ option rồi so == hoặc .equals().
   - Khi so 2 giá trị số, LUÔN ép về float trước khi so: abs(float(a) - float(b)) < 1e-6,
     KHÔNG dùng == trực tiếp giữa Rational và Float.
4. Gán is_A, is_B, is_C, is_D từ kết quả so sánh giá trị ở bước 3.
5. Ngay trước khi kết luận, in ra: print("KET_QUA:", <giá trị cuối cùng đã tính được, dạng dễ đọc
   như số, tập hợp, tọa độ — đây là giá trị THẬT, không phải chữ cái A/B/C/D>).
6. Dòng cuối: ans = "A" if is_A else "B" if is_B else "C" if is_C else "D" if is_D else "NONE"
   print("ANSWER:", ans)
   Chỉ NONE khi đã so sánh giá trị thật mà không khớp option nào.
7. Với bài toán đơn giản, ưu tiên tự suy luận đại số trực tiếp thay vì gọi hàm giải bất phương trình phức tạp.
8. Khai báo đầy đủ MỌI biến trước khi dùng.
9. Nếu option có NHIỀU điều kiện gộp lại (số + kết luận định tính như "vuông góc", "cùng phương"...),
   phải kiểm tra ĐỦ TẤT CẢ các phần đều đúng thì is_X mới True.

Đã có sẵn: from sympy import *, biến x,y,z,t,m,n,k. Không import thêm ngoài re nếu cần.
Với tập hợp dùng set/FiniteSet. Câu nhiều ý thì mọi ý phải khớp trong cùng 1 option.

{questions_block}
"""

FIX_PROMPT_TEMPLATE = """Bạn kiểm tra và sửa lại code Python/sympy đã viết trước đó cho các câu bài tập Toán 10.

Với MỖI câu bên dưới, code cũ đã chạy nhưng gặp lỗi hoặc chưa kết luận được. Hãy sửa lại đúng lỗi, giữ nguyên các quy tắc:
- BẮT BUỘC print() từng giá trị trung gian trước khi kết luận.
- So sánh bằng GIÁ TRỊ SỐ/TOÁN HỌC, không so chuỗi text nguyên văn của option.
- Nếu option là tọa độ/cặp giá trị (x, y): so từng thành phần riêng, KHÔNG trừ trực tiếp 2 tuple.
- Nếu option là tập hợp: parse thành set/FiniteSet rồi so bằng ==.
- Nếu option là khoảng nghiệm/tập nghiệm: dựng lại Interval/Union từ option rồi so == hoặc .equals(),
  KHÔNG tự đặt biến boolean diễn giải bằng lời rồi bỏ trống.
- Dòng cuối: ans = "A" if is_A else "B" if is_B else "C" if is_C else "D" if is_D else "NONE"
  print("ANSWER:", ans)
- Khai báo đầy đủ mọi biến trước khi dùng.

Đã có sẵn: from sympy import *, biến x,y,z,t,m,n,k. Không import thêm ngoài re nếu cần.

{questions_block}
"""

MAX_MISMATCH_RETRY = 2   # số lần giải bằng cách khác khi answer_code lệch answer đề

DIVERSIFY_HINTS = [
    "Hãy giải theo cách khác với lần trước: dùng phương pháp đại số trực tiếp (biến đổi tay), "
    "không gọi các hàm giải tự động như solve()/solveset().",
    "Hãy giải bằng cách thử trực tiếp: thay giá trị/tọa độ của TỪNG option vào điều kiện đề bài "
    "để kiểm tra option nào thỏa mãn, thay vì tự suy luận ra kết quả trước rồi mới so.",
    "Hãy giải lại từ đầu bằng một hướng tiếp cận khác, và kiểm tra chéo bằng ít nhất 2 cách tính "
    "khác nhau trong cùng đoạn code trước khi kết luận.",
]


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
        old_code = prev_code.get(q["id"], "")
        err = prev_error.get(q["id"], "")
        blocks.append(
            f"Câu hỏi {q['id']}: {q['question']}\n{opts}\n\n"
            f"Code đã viết trước đó:\n{old_code}\n\n"
            f"Kết quả chạy: {err}"
        )
    return "\n\n".join(blocks)

# ═════════════════════ Chạy 2 hướng ═════════════════════


def _run_code_once(batch: list, prompt: str, llm_client) -> dict:
    result = llm_client.invoke_structured(CodeSolutionBatch, [{"role": "user", "content": prompt}],
                                           max_tokens=min(1200 * len(batch), 8000))
    by_id = {s.id: s for s in result.solutions} if result else {}

    out = {}
    for q in batch:
        sol = by_id.get(q["id"])
        if not sol:
            out[q["id"]] = {"code": "", "status": "no_response", "answer": None, "raw_value": "",
                             "error": "LLM không trả code cho câu này"}
            continue

        status, raw = run_sympy_code(sol.code)
        m_ans = re.findall(r"ANSWER:\s*([ABCD]|NONE)", raw or "")
        m_val = re.findall(r"KET_QUA:\s*(.+)", raw or "")
        answer_letter = m_ans[-1] if m_ans else None
        raw_value = m_val[-1].strip() if m_val else ""

        if status != "ok":
            out[q["id"]] = {"code": sol.code, "status": status, "answer": None, "raw_value": "", "error": raw or status}
        elif not answer_letter or answer_letter == "NONE":
            out[q["id"]] = {"code": sol.code, "status": "no_answer", "answer": None, "raw_value": raw_value,
                             "error": f"Code chạy được nhưng không kết luận được option (output: {raw.strip()[:300]})"}
        else:
            out[q["id"]] = {"code": sol.code, "status": "ok", "answer": answer_letter, "raw_value": raw_value, "error": ""}
    return out

def _majority_vote(letters: list) -> tuple:
    from collections import Counter
    counts = Counter(letters)
    if not counts:
        return None, {}
    top_letter, _ = counts.most_common(1)[0]
    return top_letter, dict(counts)

def run_code_flow(batch: list, llm_client) -> dict:
    prompt = CODE_PROMPT_TEMPLATE.replace("{questions_block}", _format_code_block(batch))
    state = _run_code_once(batch, prompt, llm_client)

    # ── Lượt sửa lỗi: chỉ cho câu KHÔNG ra được kết quả (lỗi/timeout/NONE) ──
    for attempt in range(MAX_FIX_RETRY):
        need_fix = [q for q in batch if state[q["id"]]["answer"] is None]
        if not need_fix:
            break
        print(f"  [fix {attempt + 1}/{MAX_FIX_RETRY}] {len(need_fix)} câu chưa ra kết quả: {[q['id'] for q in need_fix]}")
        prev_code  = {q["id"]: state[q["id"]]["code"] for q in need_fix}
        prev_error = {q["id"]: state[q["id"]]["error"] for q in need_fix}
        fix_prompt = FIX_PROMPT_TEMPLATE.replace("{questions_block}", _format_fix_block(need_fix, prev_code, prev_error))
        state.update(_run_code_once(need_fix, fix_prompt, llm_client))

    votes = {q["id"]: [] for q in batch}
    raws  = {q["id"]: [] for q in batch}
    for q in batch:
        s = state[q["id"]]
        if s["answer"] is not None:
            votes[q["id"]].append(s["answer"])
            raws[q["id"]].append(s.get("raw_value", ""))

    # ── Lượt đa dạng hóa: chỉ cho câu ĐÃ ra kết quả nhưng LỆCH answer đề ──
    for round_idx in range(MAX_MISMATCH_RETRY):
        mismatched = [q for q in batch
                      if votes[q["id"]] and q.get("answer") and votes[q["id"]][-1] != q["answer"]]
        if not mismatched:
            break
        hint = DIVERSIFY_HINTS[round_idx % len(DIVERSIFY_HINTS)]
        print(f"  [diversify {round_idx + 1}/{MAX_MISMATCH_RETRY}] {len(mismatched)} câu lệch đề, thử cách khác: {[q['id'] for q in mismatched]}")
        div_prompt = CODE_PROMPT_TEMPLATE.replace("{questions_block}", _format_code_block(mismatched)) + f"\n\nYêu cầu thêm: {hint}"
        div_state = _run_code_once(mismatched, div_prompt, llm_client)
        for q in mismatched:
            s = div_state[q["id"]]
            if s["answer"] is not None:
                votes[q["id"]].append(s["answer"])
                raws[q["id"]].append(s.get("raw_value", ""))

    out = {}
    for q in batch:
        letters = votes[q["id"]]
        if not letters:
            out[q["id"]] = {"answer_code": "", "check": "N/A", "detail": "không lần nào ra kết quả hợp lệ"}
            continue

        top_letter, counts = _majority_vote(letters)
        raw_val = raws[q["id"]][-1] if raws[q["id"]] else ""
        total = sum(counts.values())

        if not q.get("answer"):
            out[q["id"]] = {"answer_code": raw_val, "check": "?", "detail": f"votes={counts}"}
        elif top_letter == q["answer"]:
            out[q["id"]] = {"answer_code": raw_val, "check": "✅", "detail": f"votes={counts}"}
        elif counts.get(top_letter, 0) > total / 2:
            out[q["id"]] = {"answer_code": raw_val, "check": "⚠️ nghi ngờ đề sai", "detail": f"votes={counts}"}
        else:
            out[q["id"]] = {"answer_code": raw_val, "check": "N/A (không đồng thuận)", "detail": f"votes={counts}"}
    return out


# ═════════════════════ Main ═════════════════════

def main():
    questions = _parse_questions_md(QUESTIONS_MD_PATH)

    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)

    code_result = {}
    for i in range(0, len(questions), BATCH_SIZE):
        batch = questions[i:i + BATCH_SIZE]
        code_result.update(run_code_flow(batch, llm_client))

    print(f"\n{'id':<4}{'đề':<8}{'CHECK':<24}")
    n_code_ok = 0
    for q in questions:
        r = code_result.get(q["id"], {"answer_code": "", "check": "?", "detail": ""})
        n_code_ok += int(r["check"] == "✅")
        print(f"{q['id']:<4}{q.get('answer',''):<8}{r['check']:<24}")
        print(f"     answer_code: {r['answer_code']}  |  {r['detail']}")

    print(f"\n===== TỔNG KẾT (batch={BATCH_SIZE}) =====")
    print(f"CODE : {n_code_ok}/{len(questions)} đúng")


if __name__ == "__main__":
    main()