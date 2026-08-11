# import re
# from pathlib import Path

# import json
# import sys , os 
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..","..","..")))
# from src.modules.rag.process_toan_10.chunk_lich_su_bai import _split_doan_van, _gom_doan_theo_so_tu

# # CHUNK_MARKER_RE = re.compile(r'^<!--\s*chunk\s+(\d+)\s*-\s*(\d+)\s*từ\s*-->\s*$', re.MULTILINE)
# CHUNK_MARKER_RE = re.compile(
#     r'^<!--\s*chunk\s+(\d+)\s*-\s*\(1\)\s*(\d+)\s*từ\s*\(0\)\s*(\d+)\s*từ\s*-->\s*$',
#     re.MULTILINE
# )


# MIN_WORDS = 100
# MAX_WORDS = 180

# def dem_so_tu(text: str) -> int:
#     return len(text.split())


# def tach_metadata_va_noi_dung(block: str) -> str:
#     """Nếu block bắt đầu bằng khối metadata giữa 2 dòng '---' -> trả về phần
#     nội dung SAU khối đó. Nếu không có khối metadata (chỉ 1 dòng header đơn
#     như file _chunk.md thô) -> trả về phần sau dòng đầu tiên."""
#     lines = block.splitlines()
#     if not lines:
#         return ""

#     if lines[0].strip() == "---":
#         for i in range(1, len(lines)):
#             if lines[i].strip() == "---":
#                 return "\n".join(lines[i + 1:]).strip()
#         return "\n".join(lines[1:]).strip()  # không tìm thấy '---' đóng -> fallback

#     # không có khối metadata nhiều dòng -> coi dòng đầu là header đơn (file _chunk.md thô)
#     return "\n".join(lines[1:]).strip()


# def tach_chunks(full_text: str) -> list[tuple[int, int, str, str]]:
#     matches = list(CHUNK_MARKER_RE.finditer(full_text))
#     if not matches:
#         raise ValueError("Không tìm thấy comment '<!-- chunk N - X từ -->' nào trong file.")

#     ket_qua = []
#     for i, m in enumerate(matches):
#         so_thu_tu = int(m.group(1))
#         so_tu_da_ghi = int(m.group(2))

#         start = m.end()
#         end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
#         block = re.sub(r'\n-{2,}\s*$', '', full_text[start:end]).strip()

#         header_line = block.splitlines()[0] if block.splitlines() else ""
#         noi_dung = tach_metadata_va_noi_dung(block)

#         ket_qua.append((so_thu_tu, so_tu_da_ghi, header_line, noi_dung))

#     return ket_qua


# def kiem_tra_file(input_path: Path):
#     full_text = input_path.read_text(encoding="utf-8")
#     chunks = tach_chunks(full_text)

#     print(f"Tổng số chunk tìm thấy: {len(chunks)}\n")

#     so_loi_lech, so_vuot_max, so_duoi_min = 0, 0, 0

#     for so_thu_tu, so_tu_da_ghi, header_line, noi_dung in chunks:
#         so_tu_thuc_te = dem_so_tu(noi_dung)

#         if so_tu_thuc_te != so_tu_da_ghi:
#             so_loi_lech += 1
#             print(f"❌ Chunk {so_thu_tu}: ghi {so_tu_da_ghi} từ, thực tế {so_tu_thuc_te} từ "
#                   f"| header: {header_line[:80]}")
#             continue

#         if so_tu_thuc_te > MAX_WORDS:
#             so_vuot_max += 1
#             print(f"⚠️  Chunk {so_thu_tu}: {so_tu_thuc_te} từ VƯỢT ngưỡng max ({MAX_WORDS}) "
#                   f"| header: {header_line[:80]}")
#         elif so_tu_thuc_te < MIN_WORDS:
#             so_duoi_min += 1
#             print(f"✅  Chunk {so_thu_tu}: {so_tu_thuc_te} từ DƯỚI ngưỡng min ({MIN_WORDS}) "
#                   f"| header: {header_line[:80]}")
#         else:
#             print(f"✅ Chunk {so_thu_tu}: {so_tu_thuc_te} từ — trong ngưỡng")

#     print(f"\nTổng kết:")
#     print(f"  - Sai lệch số ghi vs thực tế: {so_loi_lech}")
#     print(f"  - Vượt max ({MAX_WORDS} từ): {so_vuot_max}")
#     print(f"  - Dưới min ({MIN_WORDS} từ): {so_duoi_min}")
#     print(f"  - Đạt chuẩn: {len(chunks) - so_loi_lech - so_vuot_max - so_duoi_min}/{len(chunks)}")

# def sua_cac_chunk_vuot_nguong(input_path: Path, max_words: int = MAX_WORDS):
#     """Đọc file _chunk.md, chunk nào vượt max_words thì chia nhỏ tiếp
#     (giữ nguyên header, không cắt ngang đoạn), sau đó ghi đè lại file."""
#     full_text = input_path.read_text(encoding="utf-8")
#     chunks = tach_chunks(full_text)

#     final_parts = []
#     so_da_sua = 0

#     for so_thu_tu, so_tu_da_ghi, header_line, noi_dung in chunks:
#         so_tu_thuc_te = dem_so_tu(noi_dung)

#         if so_tu_thuc_te <= max_words:
#             final_parts.append(f"{header_line}\n{noi_dung}")
#             continue

#         so_da_sua += 1
#         doan_list = _split_doan_van(noi_dung)
#         sub_chunks = _gom_doan_theo_so_tu(doan_list, max_words=max_words)

#         if len(sub_chunks) == 1:
#             # không chia được thêm (chỉ 1 đoạn văn đơn lẻ đã tự vượt ngưỡng) -> giữ nguyên, cảnh báo
#             print(f"⚠️  Chunk {so_thu_tu} ({so_tu_thuc_te} từ) không thể chia nhỏ thêm "
#                   f"(1 đoạn văn liền không có dấu xuống dòng) — giữ nguyên.")
#             final_parts.append(f"{header_line}\n{noi_dung}")
#         else:
#             print(f"✂️  Chunk {so_thu_tu} ({so_tu_thuc_te} từ) -> chia thành {len(sub_chunks)} chunk nhỏ.")
#             for sc in sub_chunks:
#                 final_parts.append(f"{header_line}\n{sc}")

#     # ghi đè lại file với đánh số chunk mới
#     out_lines = []
#     for i, p in enumerate(final_parts, start=1):
#         noi_dung_p = "\n".join(p.splitlines()[1:])
#         so_tu = dem_so_tu(noi_dung_p)
#         out_lines.append(f"<!-- chunk {i} - {so_tu} từ -->")
#         out_lines.append(p)
#         out_lines.append("\n---\n")

#     input_path.write_text("\n".join(out_lines), encoding="utf-8")
#     print(f"\n✅ Đã sửa {so_da_sua} chunk vượt ngưỡng -> tổng {len(final_parts)} chunk -> ghi đè {input_path}")


# # if __name__ == "__main__":
# #     INPUT = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\grade_10_canh_dieu_lich_su_chu_de_7_chunk.md")
# #     kiem_tra_file(INPUT)


# if __name__ == "__main__":
#     BASE_DIR = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10")
#     TEN_GOC = "grade_10_canh_dieu_lich_su"

#     for x in range(1, 8):
#         input_path = BASE_DIR / f"{TEN_GOC}_chu_de_{x}_chunk.md"
#         if not input_path.exists():
#             print(f"⚠️ Không tìm thấy file: {input_path}\n")
#             continue

#         print(f"===== Kiểm tra chủ đề {x} =====")
#         kiem_tra_file(input_path)

#         print(f"\n----- Sửa chunk vượt ngưỡng, chủ đề {x} -----")
#         sua_cac_chunk_vuot_nguong(input_path)
#         print()


# if __name__ == "__main__":
#     BASE_DIR = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\bai")
#     TEN_GOC = "canh_dieu_ngu_van"

#     for x in range(1, 10):
#         input_path = BASE_DIR / f"{TEN_GOC}_bai_{x}_chunk.md"
#         if not input_path.exists():
#             print(f"⚠️ Không tìm thấy file: {input_path}\n")
#             continue

#         print(f"===== Kiểm tra chủ đề {x} =====")
#         kiem_tra_file(input_path)
#         print()


# --------------------- kiểm tra từ của chunk ----------------------
import re
from pathlib import Path

CHUNK_MARKER_RE = re.compile(r'^<!--\s*chunk\s+(\d+)\s*-->\s*$', re.MULTILINE)


def dem_so_tu(text: str) -> int:
    return len(text.split())


def tach_metadata_va_noi_dung(block: str) -> tuple[str, str]:
    """block bắt đầu bằng khối metadata giữa 2 dòng '---', phần còn lại là nội dung."""
    lines = block.splitlines()

    if not lines or lines[0].strip() != "---":
        return "", block.strip()

    end_meta_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_meta_idx = i
            break

    if end_meta_idx is None:
        return "", block.strip()

    metadata_text = "\n".join(lines[1:end_meta_idx])
    noi_dung = "\n".join(lines[end_meta_idx + 1:]).strip()
    return metadata_text, noi_dung


def tach_chunks(full_text: str) -> list[tuple[int, str, str]]:
    """Trả về [(số_thứ_tự, metadata_text, noi_dung), ...]."""
    matches = list(CHUNK_MARKER_RE.finditer(full_text))
    if not matches:
        return []

    ket_qua = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        block = re.sub(r'\n-{2,}\s*$', '', full_text[start:end]).strip()

        metadata_text, noi_dung = tach_metadata_va_noi_dung(block)
        so_thu_tu = int(m.group(1))
        ket_qua.append((so_thu_tu, metadata_text, noi_dung))

    return ket_qua


MAX_WORDS = 200


def dem_file(input_path: Path):
    full_text = input_path.read_text(encoding="utf-8")
    chunks = tach_chunks(full_text)

    if not chunks:
        print(f"⚠️  Không tìm thấy chunk nào trong: {input_path}")
        return

    print(f"===== {input_path.name} — {len(chunks)} chunk =====")
    for so_thu_tu, metadata_text, noi_dung in chunks:
        so_tu = dem_so_tu(noi_dung)
        icon = "✅" if so_tu <= MAX_WORDS else "⚠️"
        print(f"  {icon} chunk {so_thu_tu}: {so_tu} từ")
    print()


if __name__ == "__main__":
    BASE_DIR = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\ngu_van")
    TEN_GOC = "canh_dieu_ngu_van"

    for x in range(1, 8):
        input_path = BASE_DIR / f"{TEN_GOC}_bai_{x}_chunk_final.md"
        if not input_path.exists():
            print(f"⚠️  Không tìm thấy file: {input_path}\n")
            continue
        dem_file(input_path)