import re
from pathlib import Path

# ── Hằng số ────────────────────────────────────────────────────────
MIN_WORDS = 200
MAX_WORDS = 350

MUC_LON_ACTIVE = ["YÊU CẦU CẦN ĐẠT", "KIẾN THỨC NGỮ VĂN", "ĐỌC", "THỰC HÀNH TIẾNG VIỆT", "VIẾT"]

CHU_DE_LABEL = {
    "YÊU CẦU CẦN ĐẠT": "Yêu cầu cần đạt",
    "KIẾN THỨC NGỮ VĂN": "Kiến thức ngữ văn",
    "ĐỌC": "Đọc",
    "THỰC HÀNH TIẾNG VIỆT": "Thực hành tiếng Việt",
    "VIẾT": "Viết",
}

# ── Regex ──────────────────────────────────────────────────────────
NUM_RE      = re.compile(r'^(\d+)[\.\)]\s*(.*)$')
LETTER_RE   = re.compile(r'^([a-z])[\.\)]\s+(.*)$')
TEN_BAI_RE  = re.compile(r'^[A-ZÀ-Ỹ0-9][A-ZÀ-Ỹ0-9\s,\.\-–:\'"()]{4,}$')
ROMAN_HEADING_RE = re.compile(r'^([IVXLCDM]+)[\.\)]\s*(.*)$')

DOC_HIEU_VB_RE  = re.compile(r'^#{0,3}\s*Đọc hiểu văn bản\s*$', re.IGNORECASE | re.MULTILINE)
THUC_HANH_DH_RE = re.compile(r'^#{0,3}\s*Thực hành đọc hiểu\s*$', re.IGNORECASE | re.MULTILINE)
CHUAN_BI_RE = re.compile(r'^#{0,3}\s*\d*[\.\)]?\s*Chuẩn bị\s*[:\-]?\s*$', re.IGNORECASE | re.MULTILINE)
DOC_HIEU_RE = re.compile(r'^#{0,3}\s*\d*[\.\)]?\s*Đọc hiểu\s*[:\-]?\s*$', re.IGNORECASE | re.MULTILINE)
DINH_HUONG_RE   = re.compile(r'^#{0,3}\s*\d*\.?\s*Định hướng\s*$', re.IGNORECASE | re.MULTILINE)
THUC_HANH_VIET_RE = re.compile(r'^#{0,3}\s*\d*\.?\s*Thực hành viết\s*$', re.IGNORECASE | re.MULTILINE)


# ── Tiện ích dùng chung ──────────────────────────────────────────────


_HEADING_KEYWORDS = {"đọc hiểu", "chuẩn bị"}

def _is_heading_leftover(content: str) -> bool:
    """Mục mà nội dung chỉ là tên heading (do regex tách sót) -> loại bỏ, không coi là mục con thật."""
    return content.strip().lower() in _HEADING_KEYWORDS


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def count_words(text: str) -> int:
    return len(text.split())


def group_paragraphs_by_words(paragraphs: list[str], min_words=MIN_WORDS, max_words=MAX_WORDS) -> list[str]:
    """Gộp đoạn liên tiếp cho tới sát ngưỡng max; nếu thêm đoạn kế tiếp vượt max thì
    chốt chunk hiện tại và bắt đầu chunk mới — không cắt trong đoạn."""
    chunks, buf, buf_words = [], [], 0
    for p in paragraphs:
        w = count_words(p)
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


def split_numbered(text: str) -> list[tuple[str, str]]:
    """Tách theo '1. ...' '2. ...' ở cấp cao nhất (không đệ quy vào mục con)."""
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


def roman_to_int(s: str) -> int:
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total, prev = 0, 0
    for ch in reversed(s.upper()):
        v = vals.get(ch, 0)
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


def normalize_roman_headings(text: str) -> str:
    """I. II. III... -> 1. 2. 3... để split_numbered nhận diện đồng nhất mục con Đọc hiểu."""
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        m = ROMAN_HEADING_RE.match(stripped)
        if m and set(m.group(1).upper()) <= set("IVXLCDM"):
            out.append(f"{roman_to_int(m.group(1))}. {m.group(2)}")
        else:
            out.append(line)
    return "\n".join(out)


def make_header(so_bai: str, ten_bai: str, chu_de: str, sub: str = None) -> str:
    h = f"Bài {so_bai} {ten_bai}, {chu_de}"
    if sub:
        h += f", {sub}"
    return h + " :"


# ── Tách tác phẩm theo tên bài IN HOA (dùng cho mục ĐỌC) ─────────────

def _is_caps_title_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return bool(TEN_BAI_RE.match(stripped)) and len(stripped) < 100


def _is_subtitle_paren_line(line: str) -> bool:
    return bool(re.match(r'^\(.{2,80}\)$', line.strip()))


def _split_ten_bai_blocks(text: str) -> list[tuple[str, str]]:
    """Tách văn bản thành từng tác phẩm. Chỉ dòng IN HOA mới mở tác phẩm mới;
    dòng (...) chỉ được cộng vào tiêu đề khi đi ngay sau dòng IN HOA vừa mở,
    không được tự mở tác phẩm mới từ giữa phần thân."""
    lines = text.splitlines()
    blocks = []
    cur_title_lines, cur_body_lines = [], []
    state = "seeking_title"  # seeking_title | in_title | in_body

    def flush():
        if cur_title_lines:
            title = "\n".join(cur_title_lines).strip()
            blocks.append((title, "\n".join(cur_body_lines)))

    for line in lines:
        stripped = line.strip()

        if state == "seeking_title":
            if _is_caps_title_line(stripped):
                cur_title_lines.append(stripped)
                state = "in_title"
            continue

        if state == "in_title":
            if not stripped:
                continue
            if _is_caps_title_line(stripped) or _is_subtitle_paren_line(stripped):
                cur_title_lines.append(stripped)
                continue
            state = "in_body"
            cur_body_lines.append(line)
            continue

        # in_body: chỉ dòng IN HOA thật, đứng ngay sau dòng trống, mới mở tác phẩm mới
        if _is_caps_title_line(stripped) and (not cur_body_lines or not cur_body_lines[-1].strip()):
            flush()
            cur_title_lines, cur_body_lines = [stripped], []
            state = "in_title"
        else:
            cur_body_lines.append(line)

    flush()
    return blocks


# ── Xử lý 1 tác phẩm: Chuẩn bị -> Đọc hiểu (tách mục con) -> Câu hỏi ──

def _process_one_van_ban(title: str, body: str, so_bai: str, ten_bai: str, sub_chu_de: str) -> list[str]:
    header = make_header(so_bai, ten_bai, sub_chu_de, sub=f"tác phẩm {title}")
    chunks = []

    m_chuanbi = CHUAN_BI_RE.search(body)
    m_doc = DOC_HIEU_RE.search(body)

    if m_chuanbi and m_doc and m_doc.start() > m_chuanbi.start():
        chuan_bi_text = body[m_chuanbi.end():m_doc.start()].strip()
        doc_hieu_text = body[m_doc.end():].strip()
    elif m_doc:
        chuan_bi_text, doc_hieu_text = "", body[m_doc.end():].strip()
    else:
        chuan_bi_text, doc_hieu_text = "", body.strip()

    # gộp tên tác phẩm + Chuẩn bị thành 1 chunk duy nhất
    if chuan_bi_text:
        chunks.append(f"{header}, Chuẩn bị\n{title}\n\n{chuan_bi_text}")
    else:
        chunks.append(f"{header}\n{title}")

    if not doc_hieu_text:
        return chunks

    doc_hieu_text = normalize_roman_headings(doc_hieu_text)
    items = split_numbered(doc_hieu_text)
    items = [(label, content) for label, content in items if not _is_heading_leftover(content)]  # lọc mục rác

    if not items:
        for sub_chunk in group_paragraphs_by_words(split_paragraphs(doc_hieu_text)):
            chunks.append(f"{header}, Đọc hiểu\n{sub_chunk}")
        return chunks

    cau_hoi_start = None
    for idx in range(len(items) - 1, -1, -1):
        _, content = items[idx]
        if len(content.split('. ')) <= 3 and count_words(content) < 80:
            cau_hoi_start = idx
        else:
            break

    if cau_hoi_start is not None and len(items) - cau_hoi_start >= 3:
        main_items = items[:cau_hoi_start]
        cau_hoi_items = items[cau_hoi_start:]
    else:
        main_items = items
        cau_hoi_items = []

    for label, content in main_items:
        for sub_chunk in group_paragraphs_by_words(split_paragraphs(content)):
            chunks.append(f"{header}, Đọc hiểu, mục {label}\n{sub_chunk}")

    if cau_hoi_items:
        cau_hoi_text = "\n".join(f"{l}. {c}" for l, c in cau_hoi_items)
        chunks.append(f"{header}, Câu hỏi\n{cau_hoi_text}")

    return chunks


# ── Xử lý từng mục lớn (dispatch) ────────────────────────────────────

def handle_single(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    """Mục YÊU CẦU CẦN ĐẠT — luôn 1 chunk."""
    header = make_header(so_bai, ten_bai, chu_de)
    return [f"{header}\n{text.strip()}"]


def handle_numbered(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    """Mục KIẾN THỨC NGỮ VĂN / THỰC HÀNH TIẾNG VIỆT — tách theo 1. 2. 3..."""
    header = make_header(so_bai, ten_bai, chu_de)
    chunks = []
    for label, content in split_numbered(text):
        full = f"{label}. {content}"
        for sub_chunk in group_paragraphs_by_words(split_paragraphs(full)):
            chunks.append(f"{header}\n{sub_chunk}")
    return chunks


def handle_doc(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    chunks = []
    m1 = DOC_HIEU_VB_RE.search(text)
    m2 = THUC_HANH_DH_RE.search(text)

    if m1 and m2:
        doc_hieu_vb_text = text[m1.end():m2.start()]
        thuc_hanh_text = text[m2.end():]
    elif m1:
        doc_hieu_vb_text, thuc_hanh_text = text[m1.end():], ""
    else:
        doc_hieu_vb_text, thuc_hanh_text = text, ""

    for title, body in _split_ten_bai_blocks(doc_hieu_vb_text):
        chunks.extend(_process_one_van_ban(title, body, so_bai, ten_bai, "Đọc hiểu văn bản"))

    for title, body in _split_ten_bai_blocks(thuc_hanh_text):
        chunks.extend(_process_one_van_ban(title, body, so_bai, ten_bai, "Thực hành đọc hiểu"))

    return chunks


def handle_viet(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    chunks = []
    m1 = DINH_HUONG_RE.search(text)
    m2 = THUC_HANH_VIET_RE.search(text)

    dinh_huong_text = text[m1.end():m2.start()] if (m1 and m2) else (text[m1.end():] if m1 else "")
    thuc_hanh_text = text[m2.end():] if m2 else ""

    for sub_name, sub_text in [("Định hướng", dinh_huong_text), ("Thực hành viết", thuc_hanh_text)]:
        if not sub_text.strip():
            continue
        header = make_header(so_bai, ten_bai, chu_de, sub=sub_name)
        for label, content in split_lettered(sub_text):
            full = f"{label}. {content}"
            for sub_chunk in group_paragraphs_by_words(split_paragraphs(full)):
                chunks.append(f"{header}\n{sub_chunk}")

    return chunks


HANDLERS = {
    "YÊU CẦU CẦN ĐẠT": handle_single,
    "KIẾN THỨC NGỮ VĂN": handle_numbered,
    "ĐỌC": handle_doc,
    "THỰC HÀNH TIẾNG VIỆT": handle_numbered,
    "VIẾT": handle_viet,
}


# ── Đọc file, tách mục lớn, chạy pipeline ────────────────────────────

def extract_ten_bai_va_so(full_text: str) -> tuple[str, str]:
    lines = full_text.splitlines()
    muc_keywords = set(MUC_LON_ACTIVE)

    first_muc_idx = None
    for i, line in enumerate(lines):
        clean = line.strip().lstrip('#').strip()
        if clean in muc_keywords:
            first_muc_idx = i
            break

    if first_muc_idx is None:
        return "?", ""

    so_bai, ten_bai = "?", ""
    j = first_muc_idx - 1
    while j >= 0:
        stripped = lines[j].strip()
        if not stripped:
            j -= 1
            continue
        m = re.match(r'^#*\s*BÀI\s+(\d+)\s*$', stripped, re.IGNORECASE)
        if m:
            so_bai = m.group(1)
            break
        if not ten_bai:
            ten_bai = stripped.lstrip('#').strip()
        j -= 1

    return so_bai, ten_bai


def split_muc_lon(full_text: str) -> dict[str, str]:
    pattern = re.compile(
        r'^#{0,6}\s*(' + "|".join(re.escape(m) for m in MUC_LON_ACTIVE) + r')\s*$',
        re.MULTILINE
    )
    matches = list(pattern.finditer(full_text))
    result = {}
    for i, m in enumerate(matches):
        name = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        result[name] = full_text[start:end]
    return result


def process_file(input_path: Path) -> Path:
    full_text = input_path.read_text(encoding="utf-8")
    so_bai, ten_bai = extract_ten_bai_va_so(full_text)
    muc_dict = split_muc_lon(full_text)

    all_chunks = []
    for muc_name in MUC_LON_ACTIVE:
        body = muc_dict.get(muc_name, "").strip()
        if not body:
            continue
        handler = HANDLERS[muc_name]
        chu_de = CHU_DE_LABEL[muc_name]
        all_chunks.extend(handler(body, so_bai, ten_bai, chu_de))

    output_path = input_path.with_name(input_path.stem + "_chunk.md")
    lines = []
    for i, c in enumerate(all_chunks, start=1):
        lines.append(f"<!-- chunk {i} -->")
        lines.append(c)
        lines.append("\n---\n")
    output_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"✅ Bài {so_bai} - {ten_bai}: {len(all_chunks)} chunk -> {output_path}")
    return output_path


if __name__ == "__main__":
    INPUT = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\bai\canh_dieu_ngu_van_bai_5.md")
    process_file(INPUT)