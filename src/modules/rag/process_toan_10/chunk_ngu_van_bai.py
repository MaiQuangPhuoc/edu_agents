import re
from pathlib import Path

MON_HOC = "Môn Ngữ văn 10"
MIN_WORDS = 100
MAX_WORDS = 180

MUC_LON_ALL = [
    "YÊU CẦU CẦN ĐẠT", "KIẾN THỨC NGỮ VĂN", "ĐỌC", "THỰC HÀNH TIẾNG VIỆT",
    "VIẾT", "NÓI VÀ NGHE", "TỰ ĐÁNH GIÁ", "HƯỚNG DẪN TỰ HỌC",
]

NUM_RE           = re.compile(r'^(\d+)[\.\)]\s*(.*)$')
TOP_LEVEL_DOT_RE = re.compile(r'^(\d+)\.\s+(.*)$')
LETTER_RE        = re.compile(r'^#{0,3}\s*([a-z])[\.\)]\s*(.*)$')
TEN_BAI_RE       = re.compile(r'^[A-ZÀ-Ỹ0-9][A-ZÀ-Ỹ0-9\s,\.\-–:\'"()]{4,}$')

DOC_HIEU_VB_RE     = re.compile(r'^#{0,3}\s*Đọc hiểu văn bản\s*$', re.IGNORECASE | re.MULTILINE)
THUC_HANH_DH_RE    = re.compile(r'^#{0,3}\s*Thực hành đọc hiểu\s*$', re.IGNORECASE | re.MULTILINE)
DOC_HIEU_MARKER_RE = re.compile(r'^[^\n]{0,15}?Đọc hiểu[ \t]*$', re.IGNORECASE | re.MULTILINE)
DINH_HUONG_RE      = re.compile(r'^#{0,3}\s*\d*[\.\)]?\s*Định hướng\s*$', re.IGNORECASE | re.MULTILINE)
THUC_HANH_VIET_RE  = re.compile(r'^#{0,3}\s*\d*[\.\)]?\s*Thực hành\s*$', re.IGNORECASE | re.MULTILINE)


# ── Tiện ích dùng chung ──────────────────────────────────────────────

def dem_so_tu(text: str) -> int:
    return len(text.split())


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def gom_doan_theo_so_tu(paragraphs: list[str], min_words=MIN_WORDS, max_words=MAX_WORDS) -> list[str]:
    chunks, buf, buf_words = [], [], 0
    for p in paragraphs:
        w = dem_so_tu(p)
        if not buf:
            buf, buf_words = [p], w
        elif buf_words + w <= max_words:
            buf.append(p); buf_words += w
        else:
            chunks.append('\n\n'.join(buf))
            buf, buf_words = [p], w
    if buf:
        cuoi = '\n\n'.join(buf)
        if buf_words < min_words and chunks:
            chunks[-1] += '\n\n' + cuoi
        else:
            chunks.append(cuoi)
    return chunks


def split_numbered(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    items, cur_label, cur_lines = [], None, []
    for line in lines:
        m = NUM_RE.match(line.strip())
        if m:
            if cur_label is not None:
                items.append((cur_label, "\n".join(cur_lines).strip()))
            cur_label, cur_lines = m.group(1), [m.group(2)]
        else:
            cur_lines.append(line)
    if cur_label is not None:
        items.append((cur_label, "\n".join(cur_lines).strip()))
    return items


def split_numbered_dot_only(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    items, cur_label, cur_lines = [], None, []
    for line in lines:
        m = TOP_LEVEL_DOT_RE.match(line.strip())
        if m:
            if cur_label is not None:
                items.append((cur_label, "\n".join(cur_lines).strip()))
            cur_label, cur_lines = m.group(1), [m.group(2)]
        else:
            cur_lines.append(line)
    if cur_label is not None:
        items.append((cur_label, "\n".join(cur_lines).strip()))
    return items


def thu_thap_muc_cap_cao(text: str) -> list[tuple[int, int, str]]:
    lines = text.splitlines()
    items = []
    cur_label, cur_start, cur_lines = None, None, []
    for i, line in enumerate(lines):
        m = TOP_LEVEL_DOT_RE.match(line.strip())
        if m:
            if cur_label is not None:
                items.append((cur_label, cur_start, "\n".join(cur_lines)))
            cur_label, cur_start, cur_lines = int(m.group(1)), i, [line]
        elif cur_label is not None:
            cur_lines.append(line)
    if cur_label is not None:
        items.append((cur_label, cur_start, "\n".join(cur_lines)))
    return items


def split_lettered(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    items, cur_label, cur_lines = [], None, []
    for line in lines:
        m = LETTER_RE.match(line.strip())
        if m:
            if cur_label is not None:
                items.append((cur_label, "\n".join(cur_lines).strip()))
            cur_label, cur_lines = m.group(1), [m.group(2)]
        else:
            cur_lines.append(line)
    if cur_label is not None:
        items.append((cur_label, "\n".join(cur_lines).strip()))
    return items


def make_header(so_bai: str, ten_bai: str, chu_de: str, sub: str = None) -> str:
    h = f"{MON_HOC}, Bài {so_bai} {ten_bai}, {chu_de}"
    if sub:
        h += f", {sub}"
    return h


# ── Mục ĐỌC ────────────────────────────────────────────────────────

def tach_2_phan_doc(doc_text: str) -> tuple[str, str]:
    m1, m2 = DOC_HIEU_VB_RE.search(doc_text), THUC_HANH_DH_RE.search(doc_text)
    if m1 and m2:
        return doc_text[m1.end():m2.start()], doc_text[m2.end():]
    if m1:
        return doc_text[m1.end():], ""
    return doc_text, ""


def _la_dong_in_hoa(line: str) -> bool:
    s = line.strip().lstrip('#').strip()
    return bool(s) and bool(TEN_BAI_RE.match(s)) and len(s) < 100


def tach_cac_bai(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    bai_list, ten_hien_tai, noi_dung_hien_tai = [], None, []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if _la_dong_in_hoa(stripped):
            if ten_hien_tai is not None:
                bai_list.append((ten_hien_tai, "\n".join(noi_dung_hien_tai).strip()))
            ten_lines = [stripped.lstrip('#').strip()]
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    i += 1; continue
                if _la_dong_in_hoa(nxt) or re.match(r'^\(.{2,80}\)$', nxt):
                    ten_lines.append(nxt.lstrip('#').strip()); i += 1; continue
                break
            ten_hien_tai, noi_dung_hien_tai = "\n".join(ten_lines), []
            continue
        if ten_hien_tai is not None:
            noi_dung_hien_tai.append(lines[i])
        i += 1
    if ten_hien_tai is not None:
        bai_list.append((ten_hien_tai, "\n".join(noi_dung_hien_tai).strip()))
    return bai_list


def tach_chuan_bi(noi_dung_bai: str) -> tuple[str, str]:
    m = DOC_HIEU_MARKER_RE.search(noi_dung_bai)
    if not m:
        return "", noi_dung_bai.strip()
    return noi_dung_bai[:m.start()].strip(), noi_dung_bai[m.start():].strip()


def tim_bo_cau_hoi(phan_con_lai: str) -> tuple[str, str]:
    lines = phan_con_lai.splitlines()
    items = thu_thap_muc_cap_cao(phan_con_lai)
    if not items:
        return phan_con_lai.strip(), ""

    cut_idx, expected = None, items[-1][0]
    i = len(items) - 1
    while i >= 0:
        label, line_idx, _ = items[i]
        if label != expected:
            break
        cut_idx = i
        if expected == 1:
            break
        expected -= 1; i -= 1

    if cut_idx is None or items[i][0] != 1 or len(items) - i < 2:
        return phan_con_lai.strip(), ""

    split_line = items[cut_idx][1]
    return "\n".join(lines[:split_line]).strip(), "\n".join(lines[split_line:]).strip()


def xu_ly_1_bai_doc(ten_bai: str, noi_dung_bai: str, so_bai: str, ten_bai_lon: str, sub_chu_de: str) -> list[str]:
    header = make_header(so_bai, ten_bai_lon, sub_chu_de, sub=f"tác phẩm {ten_bai}")
    chuan_bi_text, phan_con_lai = tach_chuan_bi(noi_dung_bai)
    doc_hieu_text, cau_hoi_text = tim_bo_cau_hoi(phan_con_lai)

    parts = []
    if chuan_bi_text:
        parts.append(f"{header}, Chuẩn bị\n{ten_bai}\n\n{chuan_bi_text}")
    else:
        parts.append(f"{header}\n{ten_bai}")

    if doc_hieu_text:
        parts.append(f"{header}, Đọc hiểu\n{doc_hieu_text}")
    if cau_hoi_text:
        parts.append(f"{header}, Câu hỏi\n{cau_hoi_text}")
    else:
        print(f"[CẢNH BÁO] '{ten_bai[:50]}' không tìm được bộ câu hỏi.")

    return parts


def cut_doc(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    vb_text, th_text = tach_2_phan_doc(text)
    parts = []
    for ten, noi_dung in tach_cac_bai(vb_text):
        parts.extend(xu_ly_1_bai_doc(ten, noi_dung, so_bai, ten_bai, "Đọc hiểu văn bản"))
    for ten, noi_dung in tach_cac_bai(th_text):
        parts.extend(xu_ly_1_bai_doc(ten, noi_dung, so_bai, ten_bai, "Thực hành đọc hiểu"))
    return parts


# ── Mục VIẾT / NÓI VÀ NGHE ─────────────────────────────────────────

def tach_dinh_huong_thuc_hanh(noi_dung_bai: str) -> tuple[str, str]:
    m1, m2 = DINH_HUONG_RE.search(noi_dung_bai), THUC_HANH_VIET_RE.search(noi_dung_bai)
    if m1 and m2:
        return noi_dung_bai[m1.start():m2.start()].strip(), noi_dung_bai[m2.start():].strip()
    if m1:
        return noi_dung_bai[m1.start():].strip(), ""
    if m2:
        return "", noi_dung_bai[m2.start():].strip()
    return noi_dung_bai.strip(), ""


def xu_ly_1_de_bai(ten_de: str, noi_dung: str, so_bai: str, ten_bai_lon: str, chu_de: str) -> list[str]:
    header = make_header(so_bai, ten_bai_lon, chu_de, sub=f"đề bài {ten_de}")
    dinh_huong_text, thuc_hanh_text = tach_dinh_huong_thuc_hanh(noi_dung)
    parts = []

    for sub_name, sub_text in [("Định hướng", dinh_huong_text), ("Thực hành", thuc_hanh_text)]:
        if not sub_text.strip():
            continue
        lines = sub_text.splitlines()
        first_idx = next((i for i, l in enumerate(lines) if LETTER_RE.match(l.strip())), None)
        intro = "\n".join(lines[:first_idx]).strip() if first_idx is not None else sub_text.strip()

        items = split_lettered(sub_text)
        if not items:
            parts.append(f"{header}, {sub_name}\n{sub_text.strip()}")
            continue

        for idx, (label, content) in enumerate(items):
            if idx == 0 and intro and intro not in content:
                parts.append(f"{header}, {sub_name}\n{intro}\n\n{label}) {content}")
            else:
                parts.append(f"{header}, {sub_name}\n{label}) {content}")

    return parts if parts else [f"{header}\n{noi_dung.strip()}"]


def cut_viet_hoac_noi_nghe(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    de_bai_list = tach_cac_bai(text)
    if not de_bai_list:
        return [f"{make_header(so_bai, ten_bai, chu_de)}\n{text.strip()}"]
    parts = []
    for ten_de, noi_dung in de_bai_list:
        parts.extend(xu_ly_1_de_bai(ten_de, noi_dung, so_bai, ten_bai, chu_de))
    return parts


# ── Mục TỰ ĐÁNH GIÁ ────────────────────────────────────────────────

def normalize_circled_numbers(text: str) -> str:
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s and 0x2460 <= ord(s[0]) <= 0x2473:
            out.append(f"{ord(s[0]) - 0x2460 + 1}. {s[1:].strip()}")
        else:
            out.append(line)
    return "\n".join(out)


def tach_mo_ta_va_phan_con_lai(text: str) -> tuple[str, str, str]:
    items = thu_thap_muc_cap_cao(text)
    split_idx = next((line_idx for label, line_idx, _ in items if label == 2), None)
    if split_idx is None:
        return text.strip(), "", ""
    lines = text.splitlines()
    mo_ta = "\n".join(lines[:split_idx]).strip()
    phan_con_lai = "\n".join(lines[split_idx:]).strip()
    m = re.search(r':\s*\n?(.*?)\(', mo_ta, re.DOTALL)
    return mo_ta, (m.group(1).strip() if m else ""), phan_con_lai


def tach_noi_dung_va_cau_hoi_tdg(phan_con_lai_text: str) -> tuple[str, str]:
    lines = phan_con_lai_text.splitlines()
    items = thu_thap_muc_cap_cao(phan_con_lai_text)
    if not items:
        return phan_con_lai_text.strip(), ""

    split_line, prev_label = None, None
    for label, line_idx, _ in items:
        if prev_label is not None and label == 1 and prev_label != 1:
            split_line = line_idx
            break
        prev_label = label

    if split_line is None:
        return phan_con_lai_text.strip(), ""
    return "\n".join(lines[:split_line]).strip(), "\n".join(lines[split_line:]).strip()


def cut_tu_danh_gia(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    header = make_header(so_bai, ten_bai, chu_de)
    text = normalize_circled_numbers(text)
    mo_ta_text, ten_van_ban, phan_con_lai_text = tach_mo_ta_va_phan_con_lai(text)
    parts = []

    if mo_ta_text:
        sub = f", văn bản {ten_van_ban}" if ten_van_ban else ""
        parts.append(f"{header}{sub}\n{mo_ta_text}")
    if not phan_con_lai_text:
        return parts

    noi_dung_text, cau_hoi_text = tach_noi_dung_va_cau_hoi_tdg(phan_con_lai_text)
    if noi_dung_text:
        for label, content in split_numbered_dot_only(noi_dung_text):
            parts.append(f"{header}, Nội dung\n{label}. {content}")
    if cau_hoi_text:
        parts.append(f"{header}, Câu hỏi\n{cau_hoi_text}")
    else:
        print(f"[CẢNH BÁO] Bài {so_bai} - TỰ ĐÁNH GIÁ không tìm được bộ câu hỏi.")

    return parts


# ── Các mục đơn giản ───────────────────────────────────────────────

def cut_single(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    return [f"{make_header(so_bai, ten_bai, chu_de)}\n{text.strip()}"]


def cut_numbered(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    header = make_header(so_bai, ten_bai, chu_de)
    return [f"{header}\n{label}. {content}" for label, content in split_numbered(text)]


HANDLERS = {
    "YÊU CẦU CẦN ĐẠT": cut_single,
    "KIẾN THỨC NGỮ VĂN": cut_numbered,
    "ĐỌC": cut_doc,
    "THỰC HÀNH TIẾNG VIỆT": cut_numbered,
    "VIẾT": cut_viet_hoac_noi_nghe,
    "NÓI VÀ NGHE": cut_viet_hoac_noi_nghe,
    "TỰ ĐÁNH GIÁ": cut_tu_danh_gia,
    "HƯỚNG DẪN TỰ HỌC": cut_single,
}


# ── Hậu xử lý: chia part quá dài ───────────────────────────────────

def chia_nho_part_neu_qua_dai(part_text: str, max_words=MAX_WORDS) -> list[str]:
    lines = part_text.splitlines()
    if not lines:
        return [part_text]
    header_line = lines[0]
    noi_dung = "\n".join(lines[1:]).strip()
    if not noi_dung or dem_so_tu(noi_dung) <= max_words:
        return [part_text]
    sub_chunks = gom_doan_theo_so_tu(split_paragraphs(noi_dung), max_words=max_words)
    return [f"{header_line}\n{sc}" for sc in sub_chunks]


# ── Đọc file, chạy pipeline ────────────────────────────────────────

def extract_ten_bai_va_so(full_text: str) -> tuple[str, str]:
    lines = full_text.splitlines()
    muc_keywords = set(MUC_LON_ALL)
    first_muc_idx = next(
        (i for i, l in enumerate(lines) if l.strip().lstrip('#').strip() in muc_keywords), None
    )
    if first_muc_idx is None:
        return "?", ""

    so_bai, ten_bai = "?", ""
    j = first_muc_idx - 1
    while j >= 0:
        stripped = lines[j].strip()
        if not stripped:
            j -= 1; continue
        m = re.match(r'^#*\s*BÀI\s+(\d+)\s*$', stripped, re.IGNORECASE)
        if m:
            so_bai = m.group(1); break
        if not ten_bai:
            ten_bai = stripped.lstrip('#').strip()
        j -= 1
    return so_bai, ten_bai


def split_muc_lon(full_text: str) -> dict[str, str]:
    pattern = re.compile(r'^#{0,6}\s*(' + "|".join(re.escape(m) for m in MUC_LON_ALL) + r')\s*$', re.MULTILINE)
    matches = list(pattern.finditer(full_text))
    result = {}
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        result[m.group(1)] = full_text[start:end]
    return result


def cut_bai_muc(input_path: Path, output_dir: Path) -> Path:
    full_text = input_path.read_text(encoding="utf-8")
    so_bai, ten_bai = extract_ten_bai_va_so(full_text)
    muc_dict = split_muc_lon(full_text)

    all_parts = []
    for muc_name in MUC_LON_ALL:
        body = muc_dict.get(muc_name, "").strip()
        if body:
            all_parts.extend(HANDLERS[muc_name](body, so_bai, ten_bai, muc_name))

    final_chunks = []
    for p in all_parts:
        final_chunks.extend(chia_nho_part_neu_qua_dai(p))

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / (input_path.stem + "_chunk.md")
    out_lines = []
    for i, c in enumerate(final_chunks, start=1):
        lines_c = c.splitlines()
        header_line = lines_c[0] if lines_c else ""
        noi_dung_c = "\n".join(lines_c[1:])
        so_tu_co_header = dem_so_tu(header_line) + dem_so_tu(noi_dung_c)
        so_tu_khong_header = dem_so_tu(noi_dung_c)
        out_lines.append(f"<!-- chunk {i} - (1) {so_tu_co_header} từ (0) {so_tu_khong_header} từ -->")
        out_lines.append(c)
        out_lines.append("\n---\n")

    output_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"✅ Bài {so_bai} - {ten_bai}: {len(all_parts)} part -> {len(final_chunks)} chunk -> {output_path}")
    return output_path


if __name__ == "__main__":
    BASE_DIR = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\bai")
    OUTPUT_DIR = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\ngu_van")

    for x in range(5, 9):
        input_path = BASE_DIR / f"canh_dieu_ngu_van_bai_{x}.md"
        if not input_path.exists():
            print(f"⚠️  Không tìm thấy file: {input_path}\n")
            continue
        cut_bai_muc(input_path, OUTPUT_DIR)