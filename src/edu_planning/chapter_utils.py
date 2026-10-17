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