import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.edu_exam.curriculum import get_subject_curriculum

_ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}
_TO_ROMAN = {v: k for k, v in _ROMAN.items()}


def normalize_chapter_id(subject: str, chapter_id) -> str | None:
    """Đưa "1", "iii", "chương 4"... về đúng khóa trong curriculum của môn; None nếu không khớp."""
    valid = set(get_subject_curriculum(subject))
    s = str(chapter_id).strip().upper()
    for prefix in ("CHƯƠNG", "CHỦ ĐỀ", "BÀI"):
        s = s.replace(prefix, "")
    s = s.strip(" .:")
    if s in valid:
        return s
    num = int(s) if s.isdigit() else _ROMAN.get(s)
    if num is None:
        return None
    for cand in (str(num), _TO_ROMAN.get(num)):
        if cand in valid:
            return cand
    return None

def fix_chapters(roadmap: dict) -> list[str]:
    """Chuẩn hóa sườn theo chương trình: sửa chapter_id, bỏ bài không có thật,
    chương trống bài thì điền đủ bài của chương. Trả về danh sách ghi chú."""
    notes = []
    for gd in roadmap["giai_doan"]:
        curriculum, kept = get_subject_curriculum(gd["mon_hoc"]), []
        for ch in gd["chapters"]:
            cid = normalize_chapter_id(gd["mon_hoc"], ch["chapter_id"])
            if not cid:
                notes.append(f"Giai đoạn {gd['thu_tu']}: bỏ chương '{ch['chapter_id']}' vì không có trong chương trình")
                continue
            valid = list(curriculum[cid]["lessons"])
            lessons = [x for x in ch["lessons"] if x in valid]
            if not lessons:
                lessons = valid
                notes.append(f"Giai đoạn {gd['thu_tu']}, chương {cid}: chưa chọn bài, hệ thống lấy toàn bộ {len(valid)} bài của chương")
            kept.append({**ch, "chapter_id": cid, "lessons": lessons})
        gd["chapters"] = kept
    return notes