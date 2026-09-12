"""
File: eval_tool_selection.py
Đọc file .md dạng:

    Query 1 [Dễ]: "8 là số chẵn" là mệnh đề đúng hay sai? (xet_menh_de)

    Tool 1: xet_menh_de
    Tool 2: tinh_phuong_sai_do_lech_chuan
    Tool 3: sai_so_tuong_doi
    Tool 4: tinh_trung_vi_mode
    Tool 5: tinh_trung_binh
    ---------------------

Gom 3 query / 1 lần gọi LLM (giảm số API call từ 135 xuống ~45), dùng structured
output (Pydantic) thay vì bind_tools thô, vì mỗi query trong batch có tập
candidate tool khác nhau -> không thể bind_tools chung 1 schema cho cả 3.
System prompt mô tả rõ: thứ tự tool_name quan trọng, KHÔNG ép LLM chọn nếu
không đủ thông tin / không tool nào phù hợp.

Lưu ý: đây là eval khả năng LLM chọn tool, KHÔNG chạy qua pipeline qa_agent thật.
"""

import sys, os, re, asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from src.configs import env_config

from src.clients.llm import LLMClient
from src.edu_qa.tools.math_tools_v2_2 import TOOL_MAP_V2

INPUT_PATH = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\result_test_tool_retrival_x5_top5.md")
OUTPUT_PATH = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\result_test_tool_selection_x5_top5.md")


CHECKPOINT_SIZE = 9      # cứ gom đủ ~20 query thì ghi file 1 lần (không giảm API call)
LLM_GROUP_SIZE = 3        # số query xử lý trong 1 lần gọi LLM


# ── Structured output ────────────────────────────────────────────────────
class ToolSelection(BaseModel):
    query_id: str = Field(..., description="ID của query trong batch, đúng theo ID đã cung cấp, VD: 'Q1'")
    tool_chosen: Optional[str] = Field(
        default=None,
        description="Tên tool được chọn, PHẢI là một trong các tool candidate đã liệt kê cho query đó. "
                    "Để null nếu không có tool nào thực sự phù hợp hoặc câu hỏi thiếu dữ kiện.",
    )
    ly_do: str = Field(..., description="Giải thích ngắn gọn vì sao chọn tool này (hoặc vì sao không chọn tool nào)")
 
class BatchToolSelectionOutput(BaseModel):
    selections: list[ToolSelection] = Field(..., description="Kết quả chọn tool cho từng query trong batch, đúng số lượng và đúng query_id đã cho")
 
 
# ── System prompt (viết thẳng trong file, không tách .txt) ───────────────
SYSTEM_PROMPT = """Bạn là agent chọn công cụ (tool) tính toán Toán học lớp 10 phù hợp nhất cho từng câu hỏi.
 
Nhiệm vụ: Với MỖI query được cung cấp, bạn nhận được:
- Nội dung câu hỏi.
- Danh sách tool candidate (tên tool + mô tả chức năng), được liệt kê THEO ĐÚNG THỨ TỰ mà hệ thống
  retrieval đã xếp hạng độ liên quan (tool đứng trước có điểm liên quan ngữ nghĩa cao hơn tool đứng sau,
  nhưng thứ tự này KHÔNG đảm bảo tool đứng đầu luôn là tool đúng — bạn vẫn phải tự đọc kỹ mô tả từng tool
  để xác nhận, không được chọn máy móc theo vị trí đầu tiên).
 
Quy tắc bắt buộc:
1. Chỉ chọn 1 tool khi mô tả tool đó thực sự khớp với thao tác/loại bài toán trong câu hỏi.
2. TUYỆT ĐỐI KHÔNG được ép chọn một tool nếu:
   - Không tool nào trong danh sách candidate thực sự phù hợp với câu hỏi.
   - Câu hỏi thiếu dữ kiện cần thiết để xác định loại phép toán.
   - Câu hỏi mơ hồ, có thể khớp nhiều tool khác nhóm nghiệp vụ.
   Trong các trường hợp trên, để tool_chosen = null và giải thích lý do trong ly_do.
3. Cẩn trọng với các tool dễ gây nhầm lẫn cùng nhóm nghiệp vụ (ví dụ: trung bình vs trung vị/mode vs
   phương sai/độ lệch chuẩn; hợp vs giao vs hiệu tập hợp; định lý sin vs định lý cosin). Đọc kỹ từ khóa
   thao tác trong câu hỏi (tính trung bình, tìm trung vị, tính phương sai...) để phân loại đúng, không suy
   diễn cảm tính.
4. Trả lời đúng số lượng selections bằng đúng số query trong batch, đúng query_id đã cho, không thêm/bớt.
5. Chỉ trả lời theo đúng schema đã cung cấp, không thêm giải thích ngoài schema.
"""
 

# ── Regex parse ──────────────────────────────────────────────────────────
# Bắt toàn bộ từ "Query N [...]:" cho tới hết dòng "Result Tool: ✅ ❌ ..."
FULL_BLOCK_RE = re.compile(
    r"Query\s+\d+\s*\[[^\]]*\]:.*?Result Tool:\s*[✅❌\s]+",
    re.DOTALL,
)
# Bắt riêng phần HEADER: từ "Query N [...]:" đến ngay trước "Tool 1:"
# (câu hỏi có thể tự chứa dấu ngoặc, VD "(A ∩ B)" -> ground truth PHẢI là
# cặp ngoặc CUỐI CÙNG trong header này, không phải cặp ngoặc đầu tiên gặp được).
HEADER_RE = re.compile(
    r"Query\s+\d+\s*\[[^\]]*\]:(?P<header>.*?)Tool\s+1:",
    re.DOTALL,
)
PAREN_RE = re.compile(r"\(([^)]+)\)")
TOOL_LINE_RE = re.compile(r"Tool\s+\d+:\s*(\S+)")
 
 

def parse_blocks(text: str) -> list[dict]:
    """Parse file .md thành list các query.
 
    - Bắt toàn bộ từ 'Query N [...]:' đến hết dòng 'Result Tool: ✅ ❌ ...'.
    - Ground truth = cặp ngoặc CUỐI CÙNG trước 'Tool 1:' (không phải cặp ngoặc
      đầu tiên trong câu hỏi, vì câu hỏi có thể tự chứa dấu ngoặc, VD "(A ∩ B)").
    - In ra terminal ngay trong hàm này để kiểm tra parse đúng/sai trước khi
      chạy LLM.
    """
    items = []
    for full_match in FULL_BLOCK_RE.finditer(text):
        full_text = full_match.group(0)
 
        header_match = HEADER_RE.search(full_text)
        if not header_match:
            continue
        header = header_match.group("header")
 
        parens = PAREN_RE.findall(header)
        if not parens:
            continue
        ground_truth = parens[-1].strip()
 
        last_paren_start = header.rfind(f"({parens[-1]})")
        query_text = header[:last_paren_start].strip() if last_paren_start != -1 else header.strip()
 
        candidate_tools = TOOL_LINE_RE.findall(full_text)[:-1]
 
        if query_text and ground_truth and candidate_tools:
            items.append({
                "query_text": query_text,
                "ground_truth": ground_truth,
                "candidate_tools": candidate_tools,
            })
 
    for i, item in enumerate(items, start=1):
        # ground_truth đã được lấy đúng từ cặp ngoặc CUỐI CÙNG trước "Tool 1:".
        # Kiểm tra xem giá trị đó có nằm trong candidate_tools hay không
        # (retrieval có tìm đúng tool hay không) -> in 3 tick nếu trùng, 3 X nếu không.
        is_match = item["ground_truth"] in item["candidate_tools"]
        mark3 = "✅✅✅" if is_match else "❌❌❌"
        print(f"{i}. Query {i} ({item['ground_truth']}) -- {mark3}")
 
    print(f"\nTổng số query parse được: {len(items)}")
    return items
 
 
def test_parse_blocks_only():
    """Chạy riêng lẻ hàm parse_blocks, KHÔNG gọi LLM. Dùng để kiểm tra parse
    đúng trước khi chạy full eval.
 
    Cách chạy: python eval_tool_selection.py --parse-only
    """
    text = INPUT_PATH.read_text(encoding="utf-8")
    parse_blocks(text)
 
 
 


def classify(ground_truth: str, candidate_tools: list[str], llm_chosen: str | None) -> str:
    if ground_truth not in candidate_tools:
        return "retrieval_miss"
    if llm_chosen is None:
        return "no_tool_called"
    if llm_chosen == ground_truth:
        return "llm_correct"
    return "llm_wrong"
 
 
def _tool_description(tool_name: str) -> str:
    """Lấy docstring thật của tool trong TOOL_MAP_V2. File .md lưu tên KHÔNG có hậu tố
    '_tool' (vd 'xet_menh_de') trong khi TOOL_MAP_V2 dùng key CÓ hậu tố (vd
    'xet_menh_de_tool') -> thử cả 2 dạng trước khi kết luận không tìm thấy."""
    tool_obj = TOOL_MAP_V2.get(tool_name) or TOOL_MAP_V2.get(f"{tool_name}_tool")
    if tool_obj is None:
        print(f"  [CANH BAO] Khong tim thay tool trong TOOL_MAP_V2: {tool_name}")
        return "(không tìm thấy mô tả tool)"
    return getattr(tool_obj, "description", "") or "(không có mô tả)"
 
 
def build_group_prompt(group: list[dict]) -> str:
    """Build 1 prompt xử lý nhiều query cùng lúc (mặc định 3), giữ nguyên thứ tự tool candidate."""
    parts = []
    for idx, item in enumerate(group, start=1):
        qid = f"Q{idx}"
        tool_lines = []
        for rank, tname in enumerate(item["candidate_tools"], start=1):
            desc = _tool_description(tname)
            tool_lines.append(f"  Tool {rank} (thứ tự retrieval): {tname}\n  Mô tả: {desc}")
        tools_block = "\n".join(tool_lines)
        parts.append(
            f"--- {qid} ---\n"
            f"Câu hỏi: {item['query_text']}\n"
            f"Danh sách tool candidate (ĐÚNG THỨ TỰ retrieval, không phải thứ tự đúng/sai):\n{tools_block}"
        )
    return "\n\n".join(parts)
 
 
async def call_llm_select_tools_batch(group: list[dict], llm_client: LLMClient) -> BatchToolSelectionOutput:
    prompt_text = build_group_prompt(group)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt_text),
    ]
    result: BatchToolSelectionOutput = await llm_client.ainvoke_with_retries(
        prompt=messages,
        output_model=BatchToolSelectionOutput,
        temperature=0.0,
    )
    return result
 
 
def format_result_md(i: int, item: dict, llm_chosen: str | None, ly_do: str, status: str) -> str:
    mark = "✅✅✅✅✅" if status == "llm_correct" else "❌"
    return (
        f"## Query {i}\n"
        f"- Câu hỏi: {item['query_text']}\n"
        f"- Ground truth: `{item['ground_truth']}`\n"
        f"- Candidate tools (thứ tự): {', '.join(item['candidate_tools'])}\n"
        f"- LLM chọn: `{llm_chosen or 'KHONG_DU_THONG_TIN'}`\n"
        f"- Lý do LLM: {ly_do}\n"
        f"- Trạng thái: **{status}**\n"
        f"{mark}\n"
    )
 
 
async def run_eval_on_items(items: list[dict], output_path: Path):
    """Logic core: chạy LLM theo batch LLM_GROUP_SIZE trên 'items' đã cho, ghi
    kết quả ra 'output_path'. Dùng chung cho cả full run (135 câu) và run lại
    1 tập query cố định (VD các câu bị thiếu do hết quota)."""
    print(f"Sẽ gọi LLM {(len(items) + LLM_GROUP_SIZE - 1) // LLM_GROUP_SIZE} lần (mỗi lần {LLM_GROUP_SIZE} query)")
 
    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)

 
    output_path.write_text("", encoding="utf-8")
    counter = {"retrieval_miss": 0, "llm_correct": 0, "llm_wrong": 0, "no_tool_called": 0}
 
    pending_md = []
    for group_start in range(0, len(items), LLM_GROUP_SIZE):
        group = items[group_start:group_start + LLM_GROUP_SIZE]
        group_no = group_start // LLM_GROUP_SIZE + 1
        print(f"[call {group_no}] Query {group_start + 1}-{group_start + len(group)}/{len(items)}")
 
        try:
            batch_output = await call_llm_select_tools_batch(group, llm_client)
            selections_by_id = {s.query_id: s for s in batch_output.selections}
        except Exception as e:
            print(f"  Lỗi group {group_no}: {e}")
            for offset, item in enumerate(group):
                i = group_start + offset + 1
                pending_md.append(f"## Query {i}\n_LOI: {e}_\n")
            continue
 
        for offset, item in enumerate(group):
            i = group_start + offset + 1
            qid = f"Q{offset + 1}"
            sel = selections_by_id.get(qid)
            llm_chosen = sel.tool_chosen if sel else None
            ly_do = sel.ly_do if sel else "Khong co ket qua tra ve tu LLM cho query nay"
 
            status = classify(item["ground_truth"], item["candidate_tools"], llm_chosen)
            counter[status] += 1
            pending_md.append(format_result_md(i, item, llm_chosen, ly_do, status))
 
            mark3 = "✅✅✅" if status == "llm_correct" else "❌❌❌"
            print(f"{i}. Query {i} ({llm_chosen or 'KHONG_DU_THONG_TIN'}) -- {item['ground_truth']} -- {mark3}")
 
        # Checkpoint: cứ gom đủ CHECKPOINT_SIZE thì ghi ra file 1 lần
        if len(pending_md) >= CHECKPOINT_SIZE:
            with open(output_path, "a", encoding="utf-8") as f:
                f.write("\n---\n\n".join(pending_md) + "\n\n---\n\n")
            pending_md = []
 
    if pending_md:
        with open(output_path, "a", encoding="utf-8") as f:
            f.write("\n---\n\n".join(pending_md) + "\n\n---\n\n")
 
    # ── Tổng kết ──────────────────────────────────────────────────────────
    total = len(items)
    retrieval_hit = total - counter["retrieval_miss"]
    recall_at_k = retrieval_hit / total if total else 0
    llm_acc_given_hit = counter["llm_correct"] / retrieval_hit if retrieval_hit else 0
 
    summary = (
        f"\n# TỔNG KẾT\n"
        f"- Tổng số query: {total}\n"
        f"- Số lần gọi LLM: {(total + LLM_GROUP_SIZE - 1) // LLM_GROUP_SIZE}\n"
        f"- retrieval_miss: {counter['retrieval_miss']}\n"
        f"- llm_correct: {counter['llm_correct']}\n"
        f"- llm_wrong: {counter['llm_wrong']}\n"
        f"- no_tool_called: {counter['no_tool_called']}\n"
        f"- Retrieval Recall@k: {recall_at_k:.2%}\n"
        f"- LLM Accuracy (chỉ tính trên retrieval_hit): {llm_acc_given_hit:.2%}\n"
    )
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(summary)
 
    print(summary)
    print(f"Đã lưu kết quả vào {output_path}")
 
 
async def main():
    text = INPUT_PATH.read_text(encoding="utf-8")
    items = parse_blocks(text)
    print(f"Đọc được {len(items)} query từ {INPUT_PATH}")
    await run_eval_on_items(items, OUTPUT_PATH)
 
 
# ── Chạy lại 1 tập query cố định (VD 6 câu chưa gọi được do hết quota) ──────
async def run_missing_queries(query_numbers: list[int], output_suffix: str = "_missing"):
    """
    query_numbers: số thứ tự Query (1-based, đúng theo thứ tự parse_blocks trả về,
        VD [76, 77, 78, 85, 86, 87]).
    Lưu kết quả vào file riêng: <INPUT_PATH.stem><output_suffix>.md
    Code xử lý (build_group_prompt, call_llm_select_tools_batch, classify...) giữ
    NGUYÊN không đổi.
    """
    text = INPUT_PATH.read_text(encoding="utf-8")
    all_items = parse_blocks(text)
 
    selected_items = [all_items[n - 1] for n in query_numbers if 1 <= n <= len(all_items)]
    print(f"Chạy lại {len(selected_items)}/{len(query_numbers)} query được chỉ định: {query_numbers}")
 
    output_path = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\result_test_tool_selection_x5_top5_miss.md")
    await run_eval_on_items(selected_items, output_path)
 
 
if __name__ == "__main__":
    if "--parse-only" in sys.argv:
        test_parse_blocks_only()
    elif "--retry-missing" in sys.argv:
        # Sửa list số thứ tự query cần chạy lại tại đây
        MISSING_QUERY_NUMBERS = [76, 77, 78, 85, 86, 87]
        asyncio.run(run_missing_queries(MISSING_QUERY_NUMBERS))
    else:
        asyncio.run(main())