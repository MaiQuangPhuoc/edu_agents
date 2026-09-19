import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from src.state_edu import ExamState, QuestionSpecBatch
from src.clients.llm import LLMClient
from src.edu_exam.curriculum import format_knowledge_profile
from langchain_core.messages import AIMessage

from src.edu_qa.paths import BUILD_SPECS_PROMPT_PATH

PROMPT_PATH = BUILD_SPECS_PROMPT_PATH
VALIDATION_MAP = {
    "đạo hàm":           "sympy_derivative",
    "khảo sát":          "sympy_calculus",
    "giải phương trình": "sympy_solve",
    "bất phương trình":  "sympy_solve",
    "rút gọn":           "sympy_simplify",
    "xác suất":          "python_math",
    "thống kê":          "python_math",
    "lượng giác":        "sympy_trig",
}


def _get_validation_type(dang_bai: str) -> str:
    dang_bai_lower = dang_bai.lower()
    for keyword, vtype in VALIDATION_MAP.items():
        if keyword in dang_bai_lower:
            return vtype
    return "llm_review"


def _format_matrix_chuong(bai_hoc: list) -> str:
    lines = []
    for bai in bai_hoc:
        dk   = bai.get("do_kho", {})
        dang = bai.get("dang_bai", [])
        dang_str = ", ".join(d.get("ten", "") for d in dang) if dang and isinstance(dang[0], dict) else ", ".join(dang)
        lines.append(
            f"Bài: {bai['ten']} | {bai['so_cau']} câu | "
            f"dễ={dk.get('de',0)} trung_bình={dk.get('trung_binh',0)} khó={dk.get('kho',0)} | "
            f"Dạng bài: {dang_str}"
        )
    return "\n".join(lines)


def _format_scores_chuong(scores: dict) -> str:
    lines = []
    for lesson, sections in scores.items():
        lines.append(f"{lesson}:")
        for sec, score in sections.items():
            label = ["Không quan tâm", "Ít", "Bình thường", "Cao"][score]
            lines.append(f"  - {sec}: {score} ({label})")
    return "\n".join(lines)


def _get_chunks_chuong(retrieved_chunks: list, ch_id: str) -> str:
    chunks = [c["content"][:300] for c in retrieved_chunks if c["metadata"].get("chapter_id", "") == ch_id]
    return "\n---\n".join(chunks[:5])


def build_specs(state: ExamState, llm_client: LLMClient) -> dict:
    print(">>> [Node] build_specs")

    if state.get("specs_done", False):
        return {}

    exam_matrix       = state.get("exam_matrix", {})
    knowledge_scores  = state.get("knowledge_scores", {})
    knowledge_profile = state.get("knowledge_profile", {})
    retrieved_chunks  = state.get("retrieved_chunks", [])

    template       = PROMPT_PATH.read_text(encoding="utf-8")
    structured_llm = llm_client._llm.with_structured_output(QuestionSpecBatch)
    all_specs      = []
    id_counter     = 1

    for ch_data in exam_matrix.get("chuong", []):
        ch_id   = ch_data.get("chapter_id", "")
        ch_raw  = ch_data.get("ten", "")
        bai_hoc = ch_data.get("bai_hoc", [])

        so_cau = sum(b.get("so_cau", 0) for b in bai_hoc)
        so_de  = sum(b.get("do_kho", {}).get("de", 0) for b in bai_hoc)
        so_tb  = sum(b.get("do_kho", {}).get("trung_binh", 0) for b in bai_hoc)
        so_kho = sum(b.get("do_kho", {}).get("kho", 0) for b in bai_hoc)

        scores_ch  = knowledge_scores.get(ch_id, {})
        profile_ch = format_knowledge_profile(knowledge_profile.get(ch_id, {}))
        chunks_ch  = _get_chunks_chuong(retrieved_chunks, ch_id)

        remaining, batch_idx = so_cau, 0
        while remaining > 0:
            batch_size = min(10, remaining)
            ratio = batch_size / so_cau if so_cau > 0 else 0
            b_de  = round(so_de * ratio)
            b_tb  = round(so_tb * ratio)
            b_kho = batch_size - b_de - b_tb

            prompt = (template
                      .replace("{chuong}", ch_raw)
                      .replace("{ma_tran_chuong}", _format_matrix_chuong(bai_hoc))
                      .replace("{knowledge_scores_chuong}", _format_scores_chuong(scores_ch))
                      .replace("{knowledge_profile_chuong}", profile_ch)
                      .replace("{chunks_chuong}", chunks_ch)
                      .replace("{so_cau}", str(batch_size))
                      .replace("{so_de}", str(b_de))
                      .replace("{so_trung_binh}", str(b_tb))
                      .replace("{so_kho}", str(b_kho)))

            success = False
            for attempt in range(3):
                try:
                    result: QuestionSpecBatch = structured_llm.invoke([{"role": "user", "content": prompt}])
                    if len(result.specs) != batch_size:
                        print(f"[{ch_id}] batch {batch_idx} attempt {attempt}: {len(result.specs)}/{batch_size}, retry")
                        continue
                    for s in result.specs:
                        spec = s.model_dump()
                        spec["id"]              = id_counter
                        spec["chuong"]           = ch_raw
                        spec["chapter_id"]       = ch_id
                        spec["validation_type"]  = _get_validation_type(spec["dang_bai"])
                        id_counter += 1
                        all_specs.append(spec)
                    remaining -= len(result.specs)
                    success = True
                    break
                except Exception as e:
                    print(f"[{ch_id}] batch {batch_idx} attempt {attempt} lỗi: {e}")

            if not success:
                print(f"[{ch_id}] batch {batch_idx} thất bại sau 3 lần, bỏ qua")
                break
            batch_idx += 1

    specs_json = json.dumps(all_specs, ensure_ascii=False, indent=2)
    print(f">>> build_specs hoàn tất: {len(all_specs)} specs")

    return {
        "messages":       [AIMessage(content=specs_json)],
        "question_specs": all_specs,
        "specs_done":     len(all_specs) > 0,
        "current_step":   "build_specs",
    }