"""Resolve a PDF name to trusted lesson-plan Markdown, never extracted files."""

import re
import unicodedata
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SOURCE_ROOT = PROJECT_ROOT / "src/modules/documents/lesson_plans"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "data/auto_indexing"

SUBJECTS = {
    "toan_10": ("Toán 10", ("toan",)),
    "lich_su_10": ("Lịch sử 10", ("lich su", "suj")),
    "ngu_van_10": ("Ngữ văn 10", ("ngu van", "van")),
}
SERIES = {
    "chan_troi_sang_tao": ("chan troi sang tao", "ctst"),
    "canh_dieu": ("canh dieu", "cd"),
    "ket_noi_tri_thuc": ("ket noi tri thuc", "ket noi tri thuc voi cuoc song", "kntt"),
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFD", str(value).casefold()).replace("đ", "d")
    value = "".join(c for c in value if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def contains_words(text: str, phrase: str) -> bool:
    return f" {phrase} " in f" {text} "


def subject_from_name(filename: str) -> str:
    name = normalize(Path(filename.replace("\\", "/")).stem)
    matches = [key for key, (_, aliases) in SUBJECTS.items()
               if any(contains_words(name, alias) for alias in aliases)]
    if len(matches) != 1:
        raise ValueError("Tên PDF phải xác định đúng một môn: Toán, Lịch sử hoặc Ngữ văn.")
    grades = re.findall(r"\b(?:lop\s+)?(10|11|12)\b", name)
    if grades and any(g != "10" for g in grades):
        raise ValueError("Bản demo chỉ hỗ trợ giáo án lớp 10.")
    return matches[0]


def series_from_name(filename: str) -> str | None:
    name = normalize(Path(filename.replace("\\", "/")).stem)
    found = [key for key, aliases in SERIES.items()
             if any(contains_words(name, alias) for alias in aliases)]
    if len(found) > 1:
        raise ValueError("Tên PDF chứa nhiều bộ sách; hãy ghi rõ một bộ sách.")
    return found[0] if found else None


def read_metadata(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", text, re.S)
    if not match:
        return None
    data = yaml.safe_load(match.group(1))
    return data if isinstance(data, dict) else None


def select_sources(filename: str, source_root: Path):
    subject = subject_from_name(filename)

    # Cố định bộ sách, không lấy từ dropdown trên UI.
    base = Path(
        r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT"
        r"\src\modules\documents\lesson_plans\chan_troi_sang_tao"
    )

    folder = base / subject
    files = sorted(folder.glob("*.md"))

    if not files:
        raise ValueError(f"Không có file .md trong: {folder}")

    return subject, "chan_troi_sang_tao", [
        path.resolve() for path in files
    ]
