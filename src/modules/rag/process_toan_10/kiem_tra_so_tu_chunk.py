import re
from pathlib import Path

CHUNK_MARKER_RE = re.compile(r'^<!--\s*chunk\s+(\d+)\s*-\s*(\d+)\s*từ\s*-->\s*$', re.MULTILINE)


def dem_so_tu(text: str) -> int:
    return len(text.split())


def tach_chunks(full_text: str) -> list[tuple[int, int, str]]:
    """Trả về [(so_thu_tu, so_tu_da_ghi, noi_dung_chunk), ...].
    noi_dung_chunk = toàn bộ nội dung sau dòng comment, TRỪ dòng header đầu tiên
    (dòng 'Môn lịch sử 10, ...') — vì header không tính là nội dung."""
    matches = list(CHUNK_MARKER_RE.finditer(full_text))
    if not matches:
        raise ValueError("Không tìm thấy comment '<!-- chunk N - X từ -->' nào trong file.")

    ket_qua = []
    for i, m in enumerate(matches):
        so_thu_tu = int(m.group(1))
        so_tu_da_ghi = int(m.group(2))

        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        block = full_text[start:end]

        # loại bỏ dấu phân cách '---' cuối block nếu có
        block = re.sub(r'\n-{2,}\s*$', '', block).strip()

        lines = block.splitlines()
        header_line = lines[0] if lines else ""
        noi_dung = "\n".join(lines[1:]).strip()

        ket_qua.append((so_thu_tu, so_tu_da_ghi, header_line, noi_dung))

    return ket_qua


def kiem_tra_file(input_path: Path):
    full_text = input_path.read_text(encoding="utf-8")
    chunks = tach_chunks(full_text)

    print(f"Tổng số chunk tìm thấy: {len(chunks)}\n")

    so_loi = 0
    for so_thu_tu, so_tu_da_ghi, header_line, noi_dung in chunks:
        so_tu_thuc_te = dem_so_tu(noi_dung)

        if so_tu_thuc_te != so_tu_da_ghi:
            so_loi += 1
            print(f"❌ Chunk {so_thu_tu}: ghi {so_tu_da_ghi} từ, thực tế {so_tu_thuc_te} từ "
                  f"| header: {header_line[:80]}")
        else:
            print(f"✅ Chunk {so_thu_tu}: {so_tu_thuc_te} từ đúng khớp")

    print(f"\nTổng kết: {len(chunks) - so_loi}/{len(chunks)} chunk đúng, {so_loi} chunk sai lệch.")


# if __name__ == "__main__":
#     INPUT = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\grade_10_canh_dieu_lich_su_chu_de_7_chunk.md")
#     kiem_tra_file(INPUT)


if __name__ == "__main__":
    BASE_DIR = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10")
    TEN_GOC = "grade_10_canh_dieu_lich_su"

    for x in range(1, 8):
        input_path = BASE_DIR / f"{TEN_GOC}_chu_de_{x}_chunk.md"
        if not input_path.exists():
            print(f"⚠️ Không tìm thấy file: {input_path}\n")
            continue

        print(f"===== Kiểm tra chủ đề {x} =====")
        kiem_tra_file(input_path)
        print()