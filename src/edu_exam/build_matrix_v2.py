import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import AIMessage, HumanMessage
from src.state_edu import ExamState, ExamMatrixResponse
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

def _total_difficulty(so_cau: int, muc_tieu: float) -> dict:
    """Đề xuất tổng dễ/tb/khó cho CẢ ĐỀ (tính một lần, tổng luôn = so_cau)."""
    ratio = DIFFICULTY_RATIO[min(max(int(muc_tieu), 5), 10)]
    keys  = ["de", "trung_binh", "kho"]
    raw   = {k: so_cau * ratio[k] for k in keys}
    base  = {k: int(raw[k] + 1e-9) for k in keys}
    left  = so_cau - sum(base.values())
    for k in sorted(keys, key=lambda k: raw[k] - base[k], reverse=True)[:left]:
        base[k] += 1
    return base


def check_matrix(res, so_cau: int, tot: dict, valid_ids: list, tol: int = 1) -> list:
    """Chỉ kiểm tra. Ràng buộc cứng: tổng số câu, đủ chương. Độ khó cho lệch ±tol."""
    bai  = [b for ch in res.chuong for b in ch.bai_hoc]
    errs = []
    for ch in res.chuong:
        for b in ch.bai_hoc:
            dk = b.do_kho.de + b.do_kho.trung_binh + b.do_kho.kho
            if dk != b.so_cau:
                errs.append(f"Bài '{b.ten}': de+trung_binh+kho={dk} khác so_cau={b.so_cau}.")
            ds = sum(d.so_cau for d in b.dang_bai)
            if ds != b.so_cau:
                errs.append(f"Bài '{b.ten}': tổng dang_bai.so_cau={ds} khác so_cau={b.so_cau}.")
    n = sum(b.so_cau for b in bai)
    if n != so_cau:
        errs.append(f"Tổng số câu = {n}, cần {so_cau}: {'giảm' if n > so_cau else 'tăng'} {abs(n - so_cau)} câu.")
    got_ids = [ch.chapter_id for ch in res.chuong]
    if sorted(got_ids) != sorted(valid_ids):
        errs.append(f"chapter_id trả về {got_ids}, cần đúng {valid_ids} (mỗi chương một khối).")
    for name, key in [("dễ", "de"), ("trung bình", "trung_binh"), ("khó", "kho")]:
        got = sum(getattr(b.do_kho, key) for b in bai)
        if abs(got - tot[key]) > tol:
            errs.append(f"Số câu {name} = {got}, đề xuất {tot[key]} (lệch quá {tol}): {'giảm' if got > tot[key] else 'tăng'}.")
    return errs

# đề xuất lượng câu hỏi theo score section 
def _format_quota(scores_ch: dict, so_cau_ch: int) -> str:
    """Tính số câu đề xuất theo điểm từng section, trả về text cho prompt."""
    keys    = [(l, s) for l, secs in scores_ch.items() for s in secs]
    weights = {k: scores_ch[k[0]][k[1]] for k in keys}
    total_w = sum(weights.values()) or 1

    raw  = {k: so_cau_ch * w / total_w for k, w in weights.items()}
    base = {k: int(v) for k, v in raw.items()}
    left = so_cau_ch - sum(base.values())
    for k in sorted(raw, key=lambda k: raw[k] - base[k], reverse=True)[:left]:
        base[k] += 1

    label = ["không quan tâm", "ít quan tâm", "bình thường", "quan tâm cao"]
    count_question =  "\n".join(
        f"{lesson} | {sec} | {label[weights[(lesson, sec)]]} | đề xuất {base[(lesson, sec)]} câu"
        for lesson, sec in keys
    )
    print(f"====================== số câu đề xuất ========================\n {count_question} \n =========================\n")

    return count_question

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

    ch_dist = _calc_chapter_distribution(knowledge_scores, so_cau, muc_tieu)   # chỉ lấy ["so_cau"] làm đề xuất
    tot     = _total_difficulty(so_cau, muc_tieu)

    quota_blocks, profile_blocks = [], []
    for ch_id, dist in ch_dist.items():
        ch_raw    = get_chapter(subject, ch_id)["chapter_name"]
        scores_ch = knowledge_scores.get(ch_id, {})
        quota_blocks.append(
            f"CHƯƠNG chapter_id={ch_id}: {ch_raw} (đề xuất {dist['so_cau']} câu)\n"
            + _format_quota(scores_ch, dist["so_cau"])
        )
        profile_blocks.append(
            f"[chapter_id={ch_id}] {ch_raw}\n" + format_knowledge_profile(knowledge_profile.get(ch_id, {}))
        )

    template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = (template
              .replace("{so_cau}", str(so_cau))
              .replace("{muc_tieu_diem}", str(muc_tieu))
              .replace("{ghi_chu}", ghi_chu or "không có")
              .replace("{gop_y}", gop_y or "không có")
              .replace("{tong_do_kho_de_xuat}", f"dễ={tot['de']}, trung_bình={tot['trung_binh']}, khó={tot['kho']}")
              .replace("{de_xuat_so_cau}", "\n\n".join(quota_blocks))
              .replace("{knowledge_profile}", "\n\n".join(profile_blocks)))

    print(f"====================== PROMPT build_matrix ========================\n{prompt}\n=========================\n")
    result, errs = None, []
    for attempt in range(3):
        p = prompt if not errs else (
            prompt + "\n\nMA TRẬN LẦN TRƯỚC CÒN LỖI, HÃY SỬA CÁC LỖI SAU (giữ nguyên phần đúng):\n- " + "\n- ".join(errs)
        )
        try:
            res = llm_client.invoke_structured(ExamMatrixResponse, [{"role": "user", "content": p}], max_tokens=10000)
        except Exception as e:
            errs = [f"Output không hợp lệ: {e}"]
            print(f"[matrix] attempt {attempt} lỗi: {e}")
            continue
        if res is None:
            errs = ["Output trước không parse được. Trả JSON ngắn gọn, đủ mọi chương, không bỏ dở giữa chừng."]
            print(f"[matrix] attempt {attempt}: invoke_structured trả None")
            continue
        result = res
        errs = check_matrix(res, so_cau, tot, list(ch_dist.keys()))
        if not errs:
            break
        print(f"[matrix] attempt {attempt} còn lỗi: {errs}")

    chuong = []
    if result:
        for ch in result.chuong:
            chuong.append({
                "chapter_id": ch.chapter_id,
                "ten":        ch.ten,
                "so_cau":     sum(b.so_cau for b in ch.bai_hoc),
                "bai_hoc":    [b.model_dump() for b in ch.bai_hoc],
            })
    else:
        print("[matrix] ❌ thất bại cả 3 lần, ma trận rỗng")

    matrix = {
        "tong_so_cau": so_cau,
        "tong_do_kho": {
            "de":         sum(b["do_kho"]["de"] for c in chuong for b in c["bai_hoc"]),
            "trung_binh": sum(b["do_kho"]["trung_binh"] for c in chuong for b in c["bai_hoc"]),
            "kho":        sum(b["do_kho"]["kho"] for c in chuong for b in c["bai_hoc"]),
        },
        "chuong": chuong,
    }

    ai_message = AIMessage(content=(
        f"Ma trận đề đã được xây dựng:\n```json\n"
        f"{json.dumps(matrix, ensure_ascii=False, indent=2)}\n```\n"
        f"Bạn có góp ý gì không? (không thì 'xác nhận' để tiếp tục)"
    ))

    return {
        "messages":     [ai_message],
        "exam_matrix":  matrix,
        "gop_y_matrix": "",
        "matrix_done":  False,
        "current_step": "build_matrix",
    }