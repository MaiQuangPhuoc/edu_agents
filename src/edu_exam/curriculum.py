import json, re
from pathlib import Path

SECTIONS_PATH = Path(r'D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\curriculum_sections.json')
CURRICULUM = json.loads(SECTIONS_PATH.read_text(encoding="utf-8"))
# CURRICULUM[subject][chapter_id] = {"chapter_name": str, "lessons": {lesson_name: [section, ...]}}


def get_subject_curriculum(subject: str) -> dict:
    return CURRICULUM.get(subject, {})


def get_chapter(subject: str, chapter_id: str) -> dict:
    """Trả về {"chapter_name":..., "lessons": {...}}, raise nếu không tồn tại — tránh silent-fail."""
    ch = get_subject_curriculum(subject).get(chapter_id)
    if ch is None:
        raise ValueError(f"chapter_id '{chapter_id}' không tồn tại trong môn '{subject}'")
    return ch


def extract_chapter_ids(profile: dict, subject: str) -> list[str]:
    """Lấy list chapter_id hợp lệ từ pham_vi_kiem_tra, validate theo curriculum của môn."""
    raw = profile.get("pham_vi_kiem_tra") or profile.get("phạm_vi_kiểm_tra", "")

    if not raw:
        ho_so = profile.get("ho_so_kien_thuc") or profile.get("hồ_sơ_kiến_thức", [])
        raw = ", ".join(item.get("chu_de", "") for item in ho_so)

    valid_ids = set(get_subject_curriculum(subject).keys())
    numbers = re.findall(r'\d+', str(raw))
    return [n for n in numbers if n in valid_ids]


def map_scope(profile: dict) -> dict:
    """Từ profile (có mon_hoc + pham_vi_kiem_tra) → scope_chapters, scope_lessons theo chapter_id."""
    subject    = profile.get("mon_hoc", "")
    curriculum = get_subject_curriculum(subject)
    ids        = extract_chapter_ids(profile, subject)

    scope_chapters = {cid: curriculum[cid]["chapter_name"] for cid in ids if cid in curriculum}
    scope_lessons  = {cid: list(curriculum[cid]["lessons"].keys()) for cid in ids if cid in curriculum}

    print("------------------- mapping curriculum --------------")
    print(f"subject: {subject}\nscope_chapters: {scope_chapters}\nscope_lessons: {scope_lessons}")

    return {"scope_chapters": scope_chapters, "scope_lessons": scope_lessons}


def format_knowledge_profile(profile_ch: dict) -> str:
    """Format KnowledgeChapterProfile (dict) thành text ngắn gọn cho prompt, thay str(dict) thô."""
    if not profile_ch:
        return "Chưa có phân tích."
    return (
        f"Cần nắm: {profile_ch.get('can_nam','')}\n"
        f"Cần hiểu: {profile_ch.get('can_hieu','')}\n"
        f"Quan hệ kiến thức: {profile_ch.get('quan_he_kien_thuc','')}\n"
        f"Quan hệ dạng bài: {profile_ch.get('quan_he_dang_bai','')}"
    ) 