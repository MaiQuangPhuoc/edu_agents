import re
from pathlib import Path

SOURCE = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\grade_10_canh_dieu_lich_su.md")
OUTPUT_DIR = SOURCE.parent

KET_THUC_MARKER = "BẢNG GIẢI THÍCH THUẬT NGỮ"
CHU_DE_RE = re.compile(r'^#{0,6}\s*CHỦ ĐỀ\s+(\d+)\b.*$', re.MULTILINE | re.IGNORECASE)


def tach_3_phan(full_text: str) -> tuple[str, str, str]:
    """Trả về (phan_dau, phan_giua, phan_cuoi).
    phan_dau: trước 'CHỦ ĐỀ 1' đầu tiên.
    phan_giua: từ 'CHỦ ĐỀ 1' tới trước 'BẢNG GIẢI THÍCH THUẬT NGỮ'.
    phan_cuoi: từ 'BẢNG GIẢI THÍCH THUẬT NGỮ' tới hết."""
    matches = list(CHU_DE_RE.finditer(full_text))
    if not matches:
        raise ValueError("Không tìm thấy marker 'CHỦ ĐỀ' nào trong file nguồn.")

    idx_bat_dau = matches[0].start()
    idx_ket_thuc = full_text.find(KET_THUC_MARKER)

    phan_dau = full_text[:idx_bat_dau].strip()

    if idx_ket_thuc == -1:
        phan_giua = full_text[idx_bat_dau:].strip()
        phan_cuoi = ""
    else:
        phan_giua = full_text[idx_bat_dau:idx_ket_thuc].strip()
        phan_cuoi = full_text[idx_ket_thuc:].strip()

    return phan_dau, phan_giua, phan_cuoi


def tach_cac_chu_de(phan_giua: str) -> list[tuple[str, str]]:
    """Tách phan_giua thành từng chủ đề -> [(so_chu_de, noi_dung), ...]."""
    matches = list(CHU_DE_RE.finditer(phan_giua))
    chu_de_list = []
    for i, m in enumerate(matches):
        so_chu_de = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(phan_giua)
        chu_de_list.append((so_chu_de, phan_giua[start:end].strip()))
    return chu_de_list


def run():
    full_text = SOURCE.read_text(encoding="utf-8")
    phan_dau, phan_giua, phan_cuoi = tach_3_phan(full_text)

    # gộp phần đầu + phần cuối vào chung 1 file _gioi_thieu_sach.md
    noi_dung_gioi_thieu = phan_dau
    if phan_cuoi:
        noi_dung_gioi_thieu = f"{phan_dau}\n\n{phan_cuoi}" if phan_dau else phan_cuoi

    gioi_thieu_path = OUTPUT_DIR / f"{SOURCE.stem}_gioi_thieu_sach.md"
    gioi_thieu_path.write_text(noi_dung_gioi_thieu, encoding="utf-8")
    print(f"✅ Đã lưu: {gioi_thieu_path} ({len(noi_dung_gioi_thieu)} ký tự)")

    chu_de_list = tach_cac_chu_de(phan_giua)

    for so_chu_de, noi_dung in chu_de_list:
        output_path = OUTPUT_DIR / f"{SOURCE.stem}_chu_de_{so_chu_de}.md"
        output_path.write_text(noi_dung, encoding="utf-8")
        print(f"✅ Đã lưu: {output_path} ({len(noi_dung)} ký tự)")


if __name__ == "__main__":
    run()