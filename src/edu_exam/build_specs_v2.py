import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
# from src.state_edu import ExamState, QuestionSpecBatch
from src.state_edu import ExamState, SpecContentBatch
from src.clients.llm import LLMClient
from src.edu_exam.curriculum import format_knowledge_profile
from langchain_core.messages import AIMessage

from src.edu_qa.paths import BUILD_SPECS_PROMPT_PATH

PROMPT_PATH = BUILD_SPECS_PROMPT_PATH

BATCH_SIZE = 5


def _build_frames(bai_hoc: list, start_id: int) -> list:
    """Dựng khung câu từ ma trận: id, bai, dang_bai, do_kho. Khớp ma trận 100%."""
    frames, nid = [], start_id
    for bai in bai_hoc:
        dk    = bai.get("do_kho", {})
        diffs = ["de"] * dk.get("de", 0) + ["trung_binh"] * dk.get("trung_binh", 0) + ["kho"] * dk.get("kho", 0)
        dang  = [d for d in bai.get("dang_bai", []) if isinstance(d, dict)]
        left  = [[d["ten"], d["so_cau"]] for d in dang]
        slots = []
        while any(n > 0 for _, n in left):          # xoay vòng để mỗi dạng bài có đủ mức khó
            for item in left:
                if item[1] > 0:
                    slots.append(item[0])
                    item[1] -= 1
        diffs = diffs[::2] + diffs[1::2]
        for ten, dif in zip(slots, diffs):
            frames.append({"id": nid, "bai": bai["ten"], "dang_bai": ten, "do_kho": dif})
            nid += 1
    return frames

RANK = {"kho": 0, "trung_binh": 1, "de": 2}

def _ty_le_bai_tap(profile: dict) -> float:
    t = f"{profile.get('ghi_chu', '')} {profile.get('muc_dich', '')}".lower()
    if "lý thuyết" in t and "bài tập" not in t:
        return 0.3
    if any(k in t for k in ["bài tập", "dạng bài", "vận dụng", "tính toán"]):
        return 0.7
    return 0.5

def _assign_type(frames: list, ty_le: float) -> None:
    """Câu khó nhất -> bai_tap trước; câu dễ -> ly_thuyet."""
    n = int(len(frames) * ty_le + 0.5)
    order = sorted(range(len(frames)), key=lambda i: RANK[frames[i]["do_kho"]])
    for r, i in enumerate(order):
        frames[i]["type"] = "bai_tap" if r < n else "ly_thuyet"

def _format_frames(frames: list) -> str:
    return "\n".join(
        f"id={f['id']} | bai={f['bai']} | dang_bai={f['dang_bai']} | do_kho={f['do_kho']} | type={f['type']}"
        for f in frames
    )


def _get_chunks(retrieved_chunks: list, ch_id: str, bai_names: set) -> str:
    bl = {b.lower() for b in bai_names if b}
    ch = [c for c in retrieved_chunks if c["metadata"].get("chapter_id", "") == ch_id]
    matched = [c for c in ch
               if any(l and (b in l or l in b) for b in bl for l in [c["metadata"].get("lesson", "").lower()])]
    return "\n---\n".join(c["content"][:600] for c in (matched or ch)[:6])

def build_specs(state: ExamState, llm_client: LLMClient) -> dict:
    print(">>> [Node] build_specs")

    if state.get("specs_done", False):
        print("build_specs xong")
        return {}

    exam_matrix       = state.get("exam_matrix", {})
    knowledge_profile = state.get("knowledge_profile", {})
    retrieved_chunks  = state.get("retrieved_chunks", [])
    ty_le             = _ty_le_bai_tap(state.get("student_profile", {}))

    template   = PROMPT_PATH.read_text(encoding="utf-8")
    all_specs  = []
    id_counter = 1

    for ch_data in exam_matrix.get("chuong", []):
        ch_id  = ch_data.get("chapter_id", "")
        ch_raw = ch_data.get("ten", "")

        frames = _build_frames(ch_data.get("bai_hoc", []), id_counter)
        if not frames:
            print(f"[{ch_id}] ma trận rỗng, bỏ qua")
            continue
        _assign_type(frames, ty_le)

        n_bt = sum(1 for f in frames if f["type"] == "bai_tap")
        print(f"[{ch_id}] {len(frames)} khung: {n_bt} bai_tap, {len(frames) - n_bt} ly_thuyet")

        profile_ch = format_knowledge_profile(knowledge_profile.get(ch_id, {}))

        for i in range(0, len(frames), BATCH_SIZE):
            batch     = frames[i:i + BATCH_SIZE]
            batch_ids = {f["id"] for f in batch}
            chunks_ch = _get_chunks(retrieved_chunks, ch_id, {f["bai"] for f in batch})

            prompt = (template
                      .replace("{chuong}", ch_raw)
                      .replace("{khung_cau}", _format_frames(batch))
                      .replace("{knowledge_profile_chuong}", profile_ch)
                      .replace("{chunks_chuong}", chunks_ch)
                      .replace("{so_cau}", str(len(batch))))

            by_id = None
            for attempt in range(3):
                result = llm_client.invoke_structured(
                    SpecContentBatch, [{"role": "user", "content": prompt}], max_tokens=3000
                )
                if result and {s.id for s in result.specs} == batch_ids:
                    by_id = {s.id: s for s in result.specs}
                    break
                print(f"[{ch_id}] batch {i // BATCH_SIZE} attempt {attempt}: sai id/số lượng, retry")

            for f in batch:
                c = by_id.get(f["id"]) if by_id else None
                all_specs.append({
                    **f,                                   # id, bai, dang_bai, do_kho, type: do code chốt
                    "chuong":     ch_raw,
                    "chapter_id": ch_id,
                    "yeu_cau":    c.yeu_cau if c else f["dang_bai"],
                    "muc_dich":   c.muc_dich if c else "",
                    "ngu_canh":   c.ngu_canh if c else [],
                })

        id_counter += len(frames)

    specs_json = json.dumps(all_specs, ensure_ascii=False, indent=2)
    print(f">>> build_specs hoàn tất: {len(all_specs)} specs")

    return {
        "messages":       [AIMessage(content=specs_json)],
        "question_specs": all_specs,
        "specs_done":     len(all_specs) > 0,
        "current_step":   "build_specs",
    }