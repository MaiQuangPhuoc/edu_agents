import re
from pathlib import Path

# ══════════════════════════════════════════════════════════════════
# CẤU HÌNH ĐƯỜNG DẪN THEO TỪNG MÔN
# ══════════════════════════════════════════════════════════════════

CAU_HINH = {
    "1": {
        "ten_mon": "Lịch sử 10",
        "input_files": [
            Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10"
                 fr"\grade_10_canh_dieu_lich_su_chu_de_{x}_chunk.md")
            for x in range(1, 8)
        ],
        "output_dir": Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\lich_su"),
    },
    "2": {
        "ten_mon": "Ngữ văn 10",
        "input_files": None,
        "input_dir": Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\bai"),
        "input_pattern": "canh_dieu_ngu_van_bai_*_chunk.md",
        "output_dir": Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\ngu_van"),
    },
}


# ══════════════════════════════════════════════════════════════════
# BƯỚC 1: đọc file thô, tách từng chunk theo comment '<!-- chunk N - X từ -->'
# ══════════════════════════════════════════════════════════════════

# CHUNK_MARKER_RE = re.compile(r'^<!--\s*chunk\s+(\d+)\s*-\s*(\d+)\s*từ\s*-->\s*$', re.MULTILINE)
CHUNK_MARKER_RE = re.compile(
    r'^<!--\s*chunk\s+(\d+)\s*-\s*\(1\)\s*\d+\s*từ\s*\(0\)\s*(\d+)\s*từ\s*-->\s*$',
    re.MULTILINE
)


def tach_chunks_tho(full_text: str) -> list[str]:
    """Mỗi phần tử trả về = 1 block (dòng metadata thô + \n + nội dung),
    đã bỏ comment và dấu '---' phân cách cuối."""
    matches = list(CHUNK_MARKER_RE.finditer(full_text))
    if not matches:
        return []

    blocks = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        block = re.sub(r'\n-{2,}\s*$', '', full_text[start:end]).strip()
        if block:
            blocks.append(block)
    return blocks


def tach_dong_metadata_va_noi_dung(block: str) -> tuple[str, str]:
    """Đọc từ đầu block đến \n đầu tiên -> dòng metadata thô.
    Phần còn lại (sau \n đầu tiên) -> nội dung."""
    lines = block.splitlines()
    dong_metadata = lines[0] if lines else ""
    noi_dung = "\n".join(lines[1:]).strip()
    return dong_metadata, noi_dung


# ══════════════════════════════════════════════════════════════════
# BƯỚC 2: tách dòng metadata thô -> các trường (Môn, Chủ đề, Bài, Mục, Nội dung)
# ══════════════════════════════════════════════════════════════════

ID_CHU_DE_RE = re.compile(r'CHỦ ĐỀ\s+(\d+)', re.IGNORECASE)
ID_BAI_RE = re.compile(r'Bài\s+(\d+)', re.IGNORECASE)
ID_NOI_DUNG_RE = re.compile(r'^(\d+\.\d+)\s*(.*)$')


def parse_dong_metadata(dong_metadata: str, ten_mon: str, la_lich_su: bool) -> dict:
    parts = [p.strip() for p in dong_metadata.split(",")]

    if la_lich_su and parts and parts[0].lower().startswith("môn"):
        parts = parts[1:]

    # phát hiện 'loại' TRƯỚC khi xử lý các trường khác: nếu đoạn cuối cùng
    # là 'Câu hỏi' -> tách riêng ra, không để nó lẫn vào muc/noi_dung
    loai = "noi_dung"
    if parts and parts[-1].strip().rstrip(":").strip().lower() == "câu hỏi":
        loai = "cau_hoi"
        parts = parts[:-1]   # bỏ đoạn 'Câu hỏi' khỏi danh sách xử lý tiếp

    chu_de, bai, muc, noi_dung, id_noi_dung = "", "", "", "", ""

    for p in parts:
        p = p.rstrip(":").strip()
        if not p:
            continue
        if re.match(r'^CHỦ ĐỀ\b', p, re.IGNORECASE):
            chu_de = p
        elif re.match(r'^Bài\s+\d+', p, re.IGNORECASE):
            bai = p
        else:
            m = ID_NOI_DUNG_RE.match(p)
            if m:
                id_noi_dung = m.group(1)
                noi_dung = m.group(2).strip()
            else:
                muc = f"{muc}, {p}" if muc else p

    id_chu_de_m = ID_CHU_DE_RE.search(chu_de)
    id_bai_m = ID_BAI_RE.search(bai)

    return {
        "mon": ten_mon,
        "chu_de": chu_de,
        "id_chu_de": id_chu_de_m.group(1) if id_chu_de_m else "",
        "bai": bai,
        "id_bai": id_bai_m.group(1) if id_bai_m else "",
        "muc": muc,
        "noi_dung": noi_dung,
        "id_noi_dung": id_noi_dung,
        "loai": loai,
    }


# ══════════════════════════════════════════════════════════════════
# BƯỚC 3: tiền xử lý — chuẩn hóa nội dung
# ══════════════════════════════════════════════════════════════════

TRANG_MARKER_RE = re.compile(r'^==\s*\d+\s*==\s*$', re.MULTILINE)
MARKDOWN_HEADING_RE = re.compile(r'^#{1,6}\s*', re.MULTILINE)
KY_TU_THUA_RE = re.compile(r'[&\^@]')


def chuan_hoa_noi_dung(text: str) -> str:
    """Bỏ dòng đánh dấu trang '== N ==', tiền tố markdown heading (#, ##...),
    ký tự thừa (& ^ @). Riêng '✓' KHÔNG xoá mà thay bằng '-'."""
    text = TRANG_MARKER_RE.sub('', text)
    text = MARKDOWN_HEADING_RE.sub('', text)
    text = text.replace('✓', '-')
    text = KY_TU_THUA_RE.sub('', text)

    lines = [l.rstrip() for l in text.splitlines()]
    ket_qua, dong_trong_truoc = [], False
    for l in lines:
        if not l.strip():
            if not dong_trong_truoc:
                ket_qua.append('')
            dong_trong_truoc = True
        else:
            ket_qua.append(l.strip())
            dong_trong_truoc = False

    return "\n".join(ket_qua).strip()


# ══════════════════════════════════════════════════════════════════
# BƯỚC 4: ghi metadata dạng block, ghép 1 file hoàn chỉnh
# ══════════════════════════════════════════════════════════════════

def format_metadata_block(meta: dict) -> str:
    dong = ["---"]
    for key in ["mon", "chu_de", "id_chu_de", "bai", "id_bai", "muc", "noi_dung", "id_noi_dung", "loai"]:
        if meta.get(key):
            dong.append(f"{key}: {meta[key]}")
    dong.append("---")
    return "\n".join(dong)


def process_1_file(input_path: Path, output_path: Path, ten_mon: str, la_lich_su: bool):
    full_text = input_path.read_text(encoding="utf-8")
    blocks = tach_chunks_tho(full_text)

    if not blocks:
        print(f"⚠️  Không tìm thấy chunk nào trong: {input_path}")
        return

    out_lines = []
    for i, block in enumerate(blocks, start=1):
        dong_metadata, noi_dung_tho = tach_dong_metadata_va_noi_dung(block)
        meta = parse_dong_metadata(dong_metadata, ten_mon, la_lich_su)
        noi_dung_sach = chuan_hoa_noi_dung(noi_dung_tho)

        out_lines.append(f"<!-- chunk {i} -->")
        out_lines.append(format_metadata_block(meta))
        out_lines.append(noi_dung_sach)
        out_lines.append("\n---\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"✅ {len(blocks)} chunk -> {output_path}")


# ══════════════════════════════════════════════════════════════════
# CHẠY
# ══════════════════════════════════════════════════════════════════

def run():
    print("Chọn môn muốn xử lý:")
    print("1. Lịch sử")
    print("2. Ngữ văn")
    lua_chon = input("Nhập lựa chọn (1/2): ").strip()

    if lua_chon not in CAU_HINH:
        print("Lựa chọn không hợp lệ.")
        return

    cfg = CAU_HINH[lua_chon]
    ten_mon = cfg["ten_mon"]
    la_lich_su = (lua_chon == "1")
    output_dir = cfg["output_dir"]

    if cfg.get("input_files") is not None:
        input_files = cfg["input_files"]
    else:
        input_files = sorted(cfg["input_dir"].glob(cfg["input_pattern"]))

    if not input_files:
        print("Không tìm thấy file input nào.")
        return

    for input_path in input_files:
        if not input_path.exists():
            print(f"⚠️  Không tồn tại: {input_path}")
            continue
        output_path = output_dir / (input_path.stem + "_final.md")
        process_1_file(input_path, output_path, ten_mon, la_lich_su)


if __name__ == "__main__":
    run()