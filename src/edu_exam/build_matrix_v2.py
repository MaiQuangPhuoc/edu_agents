import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import AIMessage, HumanMessage
from src.state_edu import ExamState, ChapterMatrixResponse
from src.clients.llm import LLMClient
from src.edu_exam.curriculum import get_chapter, format_knowledge_profile
from src.edu_qa.paths import BUILD_MATRIX_PROMPT_PATH

PROMPT_PATH = BUILD_MATRIX_PROMPT_PATH

DIFFICULTY_RATIO = {
    5:  {"de": 0.70, "trung_binh": 0.25, "kho": 0.05},
    6:  {"de": 0.50, "trung_binh": 0.35, "kho": 0.15},
    7:  {"de": 0.50, "trung_binh": 0.35, "kho": 0.15},
    8:  {"de": 0.35, "trung_binh": 0.40, "kho": 0.25},
    9:  {"de": 0.20, "trung_binh": 0.30, "kho": 0.50},
    10: {"de": 0.20, "trung_binh": 0.30, "kho": 0.50},
}


def _calc_chapter_distribution(knowledge_scores: dict, so_cau: int, muc_tieu_diem: int) -> dict:
    ch_scores = {}
    for ch_id, lessons in knowledge_scores.items():
        total = sum(score for sections in lessons.values() for score in sections.values())
        ch_scores[ch_id] = total

    tong_score = sum(ch_scores.values()) or 1
    diem  = min(max(muc_tieu_diem, 5), 10)
    ratio = DIFFICULTY_RATIO.get(diem, DIFFICULTY_RATIO[7])

    result, assigned = {}, 0
    ch_ids = list(ch_scores.keys())
    for i, ch_id in enumerate(ch_ids):
        n = (so_cau - assigned) if i == len(ch_ids) - 1 else round(so_cau * ch_scores[ch_id] / tong_score)
        de  = round(n * ratio["de"])
        tb  = round(n * ratio["trung_binh"])
        kho = n - de - tb
        result[ch_id] = {"so_cau": n, "de": de, "trung_binh": tb, "kho": kho}
        assigned += n
    return result


def _format_scores_ch(scores_ch: dict) -> str:
    lines = []
    for lesson, sections in scores_ch.items():
        lines.append(f"{lesson}:")
        for sec, score in sections.items():
            label = ["Không quan tâm", "Ít", "Bình thường", "Cao"][score]
            lines.append(f"  - {sec}: {score} ({label})")
    return "\n".join(lines)


def build_matrix(state: ExamState, llm_client: LLMClient) -> dict:
    print(" ================================  file build_matrix  ================================\n"*2)

    if state.get("matrix_done", False):
        print(" matrix xonggggggggg.")
        return {"current_step": "build_matrix"}

    print("---------- chạy build_matrix với state hiện tại ---------- ")
    messages          = state.get("messages", [])
    profile           = state.get("student_profile", {})
    knowledge_scores  = state.get("knowledge_scores", {})
    knowledge_profile = state.get("knowledge_profile", {})
    gop_y             = state.get("gop_y_matrix", "")
    exam_matrix       = state.get("exam_matrix", {})
    subject           = profile.get("mon_hoc", "")

    # Đã có matrix → đang chờ góp ý từ user
    if exam_matrix and not gop_y:
        last_input = next((m.content for m in reversed(messages) if isinstance(m, HumanMessage)), "")
        if last_input.strip().lower() in ["ok", "xong", "đồng ý", "không", ""]:
            return {"matrix_done": True, "current_step": "build_matrix"}
        gop_y = last_input

    so_cau   = profile.get("so_cau_hoi", 20)
    muc_tieu = profile.get("muc_tieu_diem", 7)
    ghi_chu  = str(profile.get("ghi_chu", ""))

    ch_dist = _calc_chapter_distribution(knowledge_scores, so_cau, muc_tieu)
    template = PROMPT_PATH.read_text(encoding="utf-8")
    # structured_llm = llm_client._llm.with_structured_output(ChapterMatrixResponse)

    all_chuong = []
    for ch_id, dist in ch_dist.items():
        ch_raw     = get_chapter(subject, ch_id)["chapter_name"]
        scores_ch  = knowledge_scores.get(ch_id, {})
        profile_ch = format_knowledge_profile(knowledge_profile.get(ch_id, {}))
        # print("\n==========\n profile_ch ", profile_ch, "\n ch_raw ", ch_raw, "\n scores_ch ", scores_ch, "\n==========\n")

        prompt = (template
                  .replace("{chuong}", ch_raw)
                  .replace("{so_cau}", str(dist["so_cau"]))
                  .replace("{so_de}", str(dist["de"]))
                  .replace("{so_trung_binh}", str(dist["trung_binh"]))
                  .replace("{so_kho}", str(dist["kho"]))
                  .replace("{muc_tieu_diem}", str(muc_tieu))
                  .replace("{ghi_chu}", ghi_chu)
                  .replace("{knowledge_scores_ch}", _format_scores_ch(scores_ch))
                  .replace("{knowledge_profile_ch}", profile_ch)
                  .replace("{gop_y}", gop_y or "không có"))

        bai_hoc = []
        for attempt in range(3):
            try:
                # result: ChapterMatrixResponse = structured_llm.invoke([{"role": "user", "content": prompt}])
                result = llm_client.invoke_structured(ChapterMatrixResponse, [{"role": "user", "content": prompt}], max_tokens=3000)
                total = sum(b.so_cau for b in result.bai_hoc)
                if total == dist["so_cau"]:
                    bai_hoc = [b.model_dump() for b in result.bai_hoc]
                    break
                print(f"[{ch_id}] attempt {attempt}: tổng {total} != {dist['so_cau']}, retry")
            except Exception as e:
                print(f"[{ch_id}] attempt {attempt} lỗi: {e}")

        all_chuong.append({
            "chapter_id": ch_id,
            "ten":        ch_raw,
            "so_cau":     dist["so_cau"],
            "bai_hoc":    bai_hoc,
        })

    matrix = {
        "tong_so_cau": so_cau,
        "tong_do_kho": {
            "de":         sum(d["de"] for d in ch_dist.values()),
            "trung_binh": sum(d["trung_binh"] for d in ch_dist.values()),
            "kho":        sum(d["kho"] for d in ch_dist.values()),
        },
        "chuong": all_chuong,
    }

    ai_message = AIMessage(content=(
        f"Ma trận đề đã được xây dựng:\n```json\n"
        f"{json.dumps(matrix, ensure_ascii=False, indent=2)}\n```\n"
        f"Bạn có góp ý gì không? (gõ 'ok' để tiếp tục)"
    ))

    return {
        "messages":     [ai_message],
        "exam_matrix":  matrix,
        "gop_y_matrix": "",
        "matrix_done":  False,
        "current_step": "build_matrix",
    }