import re
from pathlib import Path

MON_HOC = "Môn lịch sử 10"

CHU_DE_LINE_RE = re.compile(r'^.*CHỦ ĐỀ.*$', re.MULTILINE | re.IGNORECASE)
# CHU_DE_LINE_RE = re.compile(r'^CHỦ ĐỀ\s+\d+\s*:\s*.+$', re.MULTILINE | re.IGNORECASE)
BAI_RE = re.compile(r'^Bài\s+(\d+)\s*:?\s*(.+)$', re.MULTILINE)

MUC_TIEU_MARKER_RE = re.compile(r'^Học xong bài này,\s*em sẽ\s*:?\s*$', re.IGNORECASE | re.MULTILINE)
CHECK_MARK = '✓'
MUC_SO_NGUYEN_RE = re.compile(r'^#{0,3}\s*(\d+)\.(?!\d)\s+(.*)$')

# CAU_HOI_MUC_MARKER_RE = re.compile(r'^Đọc thông tin.*$', re.IGNORECASE | re.MULTILINE)
CAU_HOI_MUC_MARKER_RE = re.compile(r'^\??\s*Đọc thông tin.*$', re.IGNORECASE | re.MULTILINE)

MIN_WORDS = 200
MAX_WORDS = 350


def _dem_so_tu(text: str) -> int:
    return len(text.split())


def _split_doan_van(text: str) -> list[str]:
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def _gom_doan_theo_so_tu(paragraphs: list[str], min_words=MIN_WORDS, max_words=MAX_WORDS) -> list[str]:
    """Gộp đoạn liên tiếp tới sát ngưỡng max; nếu thêm đoạn kế tiếp vượt max thì
    chốt chunk hiện tại, không cắt trong đoạn."""
    chunks, buf, buf_words = [], [], 0
    for p in paragraphs:
        w = _dem_so_tu(p)
        if not buf:
            buf, buf_words = [p], w
        elif buf_words + w <= max_words:
            buf.append(p)
            buf_words += w
        else:
            chunks.append('\n\n'.join(buf))
            buf, buf_words = [p], w
    if buf:
        chunks.append('\n\n'.join(buf))
    return chunks


def chia_nho_part_neu_qua_dai(part_text: str, max_words=MAX_WORDS) -> list[str]:
    """part_text = header_line + '\n' + nội dung.
    Header (kể cả phần cuối như ', Câu hỏi') LUÔN được giữ nguyên và lặp lại
    ở mỗi chunk con khi bị tách. Nếu nội dung không vượt ngưỡng -> giữ nguyên 1 chunk."""
    lines = part_text.splitlines()
    if not lines:
        return [part_text]

    header_line = lines[0]
    noi_dung = "\n".join(lines[1:]).strip()

    if not noi_dung or _dem_so_tu(noi_dung) <= max_words:
        return [part_text]

    doan_list = _split_doan_van(noi_dung)
    sub_chunks = _gom_doan_theo_so_tu(doan_list, max_words=max_words)

    return [f"{header_line}\n{sc}" for sc in sub_chunks]

def _muc_con_re_cho(so_muc: str) -> re.Pattern:
    """Tạo regex mục con khớp đúng số cha, VD so_muc='1' -> khớp '1.1', '1.2'..."""
    return re.compile(rf'^#{{0,3}}\s*{re.escape(so_muc)}\.(\d+)\.?\s+(.*)$')

def tach_muc_con(so_muc: str, noi_dung_muc: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Trả về (phan_dau_text, [(so_muc_con, tieu_de_con, noi_dung_con), ...]).
    phan_dau_text = phần đầu mục lớn trước mục con đầu tiên (hoặc toàn bộ nếu
    không có mục con nào). Chỉ nhận mục con có số cha khớp đúng so_muc
    (VD mục '1' chỉ nhận '1.1', '1.2', không nhận '2.1')."""
    pattern = _muc_con_re_cho(so_muc)
    lines = noi_dung_muc.splitlines()

    starts = []
    for i, line in enumerate(lines):
        m = pattern.match(line)
        if m:
            starts.append((m.group(1), m.group(2).strip(), i))

    if not starts:
        return noi_dung_muc.strip(), []

    phan_dau_text = "\n".join(lines[:starts[0][2]]).strip()

    muc_con_list = []
    for i, (so_con, tieu_de_con, line_idx) in enumerate(starts):
        end_idx = starts[i + 1][2] if i + 1 < len(starts) else len(lines)
        noi_dung_con = "\n".join(lines[line_idx:end_idx]).strip()
        muc_con_list.append((so_con, tieu_de_con, noi_dung_con))

    return phan_dau_text, muc_con_list

def tach_cau_hoi(noi_dung: str) -> tuple[str, str]:
    """Trả về (noi_dung_chinh, cau_hoi_text). Nếu không tìm thấy marker
    'Đọc thông tin...' -> cau_hoi_text rỗng, giữ nguyên noi_dung_chinh."""
    m = CAU_HOI_MUC_MARKER_RE.search(noi_dung)
    if not m:
        return noi_dung.strip(), ""

    noi_dung_chinh = noi_dung[:m.start()].strip()
    cau_hoi_text = noi_dung[m.start():].strip()
    return noi_dung_chinh, cau_hoi_text

def tach_muc_tieu(noi_dung_bai: str) -> tuple[str, str]:
    """Trả về (muc_tieu_text, phan_con_lai_text).
    muc_tieu_text = dòng marker + các dòng liên tiếp có chứa ✓.
    Dừng lại ngay khi gặp 1 dòng không rỗng mà KHÔNG chứa ✓."""
    m = MUC_TIEU_MARKER_RE.search(noi_dung_bai)
    if not m:
        return "", noi_dung_bai.strip()

    lines = noi_dung_bai[m.start():].splitlines()
    muc_tieu_lines = [lines[0]]  # dòng marker
    cut_idx = 1

    for i in range(1, len(lines)):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            muc_tieu_lines.append(line)
            cut_idx = i + 1
            continue
        if CHECK_MARK in stripped:
            muc_tieu_lines.append(line)
            cut_idx = i + 1
        else:
            break

    muc_tieu_text = "\n".join(muc_tieu_lines).strip()
    phan_con_lai_text = noi_dung_bai[m.start():] 
    phan_con_lai_text = "\n".join(lines[cut_idx:]).strip()

    phan_truoc = noi_dung_bai[:m.start()]
    return muc_tieu_text, (phan_truoc + "\n" + phan_con_lai_text).strip() if phan_truoc.strip() else phan_con_lai_text

def tach_mo_ta_va_cac_muc(phan_con_lai: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Trả về (mo_ta_text, [(so_muc, tieu_de, noi_dung), ...]).
    Dùng 2 tầng đếm để tránh nhầm lẫn khi 1 mục lớn chứa bên trong 1 danh sách
    con cũng đánh số reset lại từ 1 — nếu không xử lý, số của danh sách con
    có thể trùng ngẫu nhiên với số mục lớn tiếp theo đang chờ, gây tách sai."""
    lines = phan_con_lai.splitlines()

    raw_starts = []
    for i, line in enumerate(lines):
        m = MUC_SO_NGUYEN_RE.match(line)
        if m:
            raw_starts.append((int(m.group(1)), m.group(2).strip(), i))

    if not raw_starts:
        return phan_con_lai.strip(), []

    starts = [raw_starts[0]]
    dinh_expected = raw_starts[0][0] + 1
    trong_nested = False
    local_next = None

    for so_muc, tieu_de, line_idx in raw_starts[1:]:
        if trong_nested and so_muc == local_next:
            # vẫn đang tiếp nối danh sách con -> bỏ qua, KHÔNG kiểm tra top-level
            local_next += 1
            continue

        trong_nested = False  # thoát (hoặc chưa từng vào) chế độ nested

        if so_muc == dinh_expected:
            starts.append((so_muc, tieu_de, line_idx))
            dinh_expected += 1
        else:
            # không khớp mục lớn tiếp theo -> coi là bắt đầu 1 danh sách con (reset)
            trong_nested = True
            local_next = so_muc + 1

    mo_ta_text = "\n".join(lines[:starts[0][2]]).strip()

    muc_list = []
    for i, (so_muc, tieu_de, line_idx) in enumerate(starts):
        end_idx = starts[i + 1][2] if i + 1 < len(starts) else len(lines)
        noi_dung = "\n".join(lines[line_idx:end_idx]).strip()
        muc_list.append((str(so_muc), tieu_de, noi_dung))

    return mo_ta_text, muc_list

def xu_ly_1_bai_lich_su(so_bai: str, ten_bai: str, noi_dung_bai: str, dong_chu_de: str) -> list[str]:
    header_base = f"{MON_HOC}, {dong_chu_de}, Bài {so_bai}: {ten_bai}"

    muc_tieu_text, phan_con_lai = tach_muc_tieu(noi_dung_bai)
    mo_ta_text, muc_list = tach_mo_ta_va_cac_muc(phan_con_lai)

    parts = []
    if muc_tieu_text:
        parts.append(f"{header_base}, Mục tiêu\n{muc_tieu_text}")

    if mo_ta_text:
        parts.append(f"{header_base}, Mô tả bài\n{mo_ta_text}")

    for so_muc, tieu_de, noi_dung_muc in muc_list:
        header_muc = f"{header_base}, Mục {so_muc} {tieu_de}"
        phan_dau_text, muc_con_list = tach_muc_con(so_muc, noi_dung_muc)

        if not muc_con_list:
            # không có mục con -> tách câu hỏi trực tiếp trong mục lớn
            noi_dung_chinh, cau_hoi_text = tach_cau_hoi(phan_dau_text)
            if noi_dung_chinh:
                parts.append(f"{header_muc}\n{noi_dung_chinh}")
            if cau_hoi_text:
                parts.append(f"{header_muc}, Câu hỏi\n{cau_hoi_text}")
        else:
            # có mục con -> mục con ĐẦU TIÊN gộp chung với phần đầu mục lớn thành 1 part,
            # các mục con TỪ THỨ 2 trở đi mới tách riêng
            muc_con_dau, *muc_con_con_lai = muc_con_list

            so_con_dau, tieu_de_con_dau, noi_dung_con_dau = muc_con_dau
            noi_dung_gop = f"{phan_dau_text}\n{noi_dung_con_dau}".strip() if phan_dau_text else noi_dung_con_dau

            noi_dung_chinh, cau_hoi_text = tach_cau_hoi(noi_dung_gop)
            if noi_dung_chinh:
                parts.append(f"{header_muc}\n{noi_dung_chinh}")
            if cau_hoi_text:
                parts.append(f"{header_muc}, Câu hỏi\n{cau_hoi_text}")

            for so_con, tieu_de_con, noi_dung_con in muc_con_con_lai:
                header_con = f"{header_muc}, {so_muc}.{so_con} {tieu_de_con}"
                noi_dung_chinh, cau_hoi_text = tach_cau_hoi(noi_dung_con)
                if noi_dung_chinh:
                    parts.append(f"{header_con}\n{noi_dung_chinh}")
                if cau_hoi_text:
                    parts.append(f"{header_con}, Câu hỏi\n{cau_hoi_text}")

    return parts


def lay_dong_chu_de(full_text: str) -> str:
    """Lấy dòng đầu tiên chứa 'CHỦ ĐỀ ...' trong file."""
    m = CHU_DE_LINE_RE.search(full_text)
    if not m:
        raise ValueError("Không tìm thấy dòng 'CHỦ ĐỀ ...' trong file.")
    return m.group(0).strip()


def tach_cac_bai(full_text: str) -> list[tuple[str, str, str]]:
    """Tách theo 'Bài X: TÊN BÀI' -> [(so_bai, ten_bai, noi_dung), ...]."""
    matches = list(BAI_RE.finditer(full_text))
    if not matches:
        raise ValueError("Không tìm thấy 'Bài X: ...' nào trong file.")

    bai_list = []
    for i, m in enumerate(matches):
        so_bai = m.group(1)
        ten_bai = m.group(2).strip()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        noi_dung = full_text[start:end].strip()
        bai_list.append((so_bai, ten_bai, noi_dung))

    return bai_list


def process_file(input_path: Path) -> Path:
    full_text = input_path.read_text(encoding="utf-8")

    dong_chu_de = lay_dong_chu_de(full_text)
    bai_list = tach_cac_bai(full_text)

    all_parts = []
    for so_bai, ten_bai, noi_dung_bai_raw in bai_list:
        noi_dung_bai = "\n".join(noi_dung_bai_raw.splitlines()[1:]).strip()
        all_parts.extend(xu_ly_1_bai_lich_su(so_bai, ten_bai, noi_dung_bai, dong_chu_de))

    # hậu xử lý: chia part quá dài thành chunk nhỏ, giữ nguyên header ở mỗi chunk
    final_chunks = []
    for p in all_parts:
        final_chunks.extend(chia_nho_part_neu_qua_dai(p))

    output_path = input_path.with_name(input_path.stem + "_chunk.md")
    out_lines = []
    for i, c in enumerate(final_chunks, start=1):
        noi_dung = "\n".join(c.splitlines()[1:])
        so_tu = _dem_so_tu(noi_dung)
        out_lines.append(f"<!-- chunk {i} - {so_tu} từ -->")
        out_lines.append(c)
        out_lines.append("\n---\n")

    output_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"✅ {dong_chu_de}: {len(bai_list)} bài -> {len(all_parts)} part gốc -> {len(final_chunks)} chunk cuối -> {output_path}")
    return output_path


# if __name__ == "__main__":
#     INPUT = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\grade_10_canh_dieu_lich_su_chu_de_1.md")
#     process_file(INPUT)

if __name__ == "__main__":
    BASE_DIR = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10")
    TEN_GOC = "grade_10_canh_dieu_lich_su"

    for x in range(1, 8):
        input_path = BASE_DIR / f"{TEN_GOC}_chu_de_{x}.md"
        if not input_path.exists():
            print(f"⚠️ Không tìm thấy file: {input_path}\n")
            continue

        print(f"===== Xử lý chủ đề {x} =====")
        process_file(input_path)
        print()