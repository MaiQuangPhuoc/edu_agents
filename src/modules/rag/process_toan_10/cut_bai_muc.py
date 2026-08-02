import re
from pathlib import Path

from matplotlib import lines

# ── 8 mục lớn ──────────────────────────────────────────────────────
MUC_LON_ALL = [
    "YÊU CẦU CẦN ĐẠT", "KIẾN THỨC NGỮ VĂN", "ĐỌC", "THỰC HÀNH TIẾNG VIỆT",
    "VIẾT", "NÓI VÀ NGHE", "TỰ ĐÁNH GIÁ", "HƯỚNG DẪN TỰ HỌC",
]

NUM_RE       = re.compile(r'^(\d+)[\.\)]\s*(.*)$')
TEN_BAI_RE   = re.compile(r'^[A-ZÀ-Ỹ0-9][A-ZÀ-Ỹ0-9\s,\.\-–:\'"()]{4,}$')
DOC_HIEU_VB_RE  = re.compile(r'^#{0,3}\s*Đọc hiểu văn bản\s*$', re.IGNORECASE | re.MULTILINE)
THUC_HANH_DH_RE = re.compile(r'^#{0,3}\s*Thực hành đọc hiểu\s*$', re.IGNORECASE | re.MULTILINE)
# DOC_HIEU_MARKER_RE = re.compile(r'^\s*2?[\.\)]?\s*Đọc hiểu\s*$', re.IGNORECASE | re.MULTILINE)
DOC_HIEU_MARKER_RE = re.compile(r'^[^\n]{0,15}?Đọc hiểu[ \t]*$', re.IGNORECASE | re.MULTILINE)

def make_header(so_bai: str, ten_bai: str, chu_de: str, sub: str = None) -> str:
    h = f"Bài {so_bai} {ten_bai}, {chu_de}"
    if sub:
        h += f", {sub}"
    return h + " :"


# ── BƯỚC 1: tách mục ĐỌC thành 2 biến: Đọc hiểu văn bản / Thực hành đọc hiểu ──

def tach_2_phan_doc(doc_text: str) -> tuple[str, str]:
    """Trả về (doc_hieu_van_ban_text, thuc_hanh_doc_hieu_text)."""
    m1 = DOC_HIEU_VB_RE.search(doc_text)
    m2 = THUC_HANH_DH_RE.search(doc_text)

    if m1 and m2:
        doc_hieu_van_ban_text = doc_text[m1.end():m2.start()]
        thuc_hanh_doc_hieu_text = doc_text[m2.end():]
    elif m1:
        doc_hieu_van_ban_text = doc_text[m1.end():]
        thuc_hanh_doc_hieu_text = ""
    else:
        doc_hieu_van_ban_text = doc_text
        thuc_hanh_doc_hieu_text = ""

    return doc_hieu_van_ban_text, thuc_hanh_doc_hieu_text


# ── BƯỚC 2: tách 1 biến thành danh sách các bài, dựa vào tên IN HOA ──

def tach_cac_bai(text: str) -> list[tuple[str, str]]:
    """Gặp dòng IN HOA -> bắt đầu 1 bài mới. Trả về [(ten_bai, noi_dung_bai), ...]."""
    lines = text.splitlines()
    bai_list = []
    ten_bai_hien_tai = None
    noi_dung_hien_tai = []

    def la_dong_in_hoa(line: str) -> bool:
        s = line.strip().lstrip('#').strip()   # bỏ '#' markdown trước khi kiểm tra IN HOA
        return bool(s) and bool(TEN_BAI_RE.match(s)) and len(s) < 100

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if la_dong_in_hoa(stripped):
            if ten_bai_hien_tai is not None:
                bai_list.append((ten_bai_hien_tai, "\n".join(noi_dung_hien_tai).strip()))

            ten_lines = [stripped.lstrip('#').strip()]   # <-- bỏ '#' khi lưu
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    i += 1
                    continue
                if la_dong_in_hoa(nxt) or re.match(r'^\(.{2,80}\)$', nxt):
                    ten_lines.append(nxt.lstrip('#').strip())   # <-- bỏ '#' khi lưu
                    i += 1
                    continue
                break
            ten_bai_hien_tai = "\n".join(ten_lines)
            noi_dung_hien_tai = []
            continue
 

        if ten_bai_hien_tai is not None:
            noi_dung_hien_tai.append(line)
        i += 1

    if ten_bai_hien_tai is not None:
        bai_list.append((ten_bai_hien_tai, "\n".join(noi_dung_hien_tai).strip()))

    return bai_list


# ── BƯỚC 3: trong 1 bài, tách "Chuẩn bị" khỏi phần còn lại (từ "Đọc hiểu") ──

def tach_chuan_bi(noi_dung_bai: str) -> tuple[str, str]:
    """Trả về (chuan_bi_text, phan_con_lai_text). phan_con_lai bắt đầu từ chính dòng 'Đọc hiểu'.
    Nếu không tìm được marker 'Đọc hiểu' -> coi toàn bộ là phan_con_lai (giữ hành vi cũ)."""
    m = DOC_HIEU_MARKER_RE.search(noi_dung_bai)
    if not m:
        return "", noi_dung_bai.strip()

    chuan_bi_text = noi_dung_bai[:m.start()].strip()
    phan_con_lai = noi_dung_bai[m.start():].strip()
    return chuan_bi_text, phan_con_lai


# ── BƯỚC 4: hàm riêng tìm bộ câu hỏi trong phần còn lại ──

def tim_bo_cau_hoi(phan_con_lai: str) -> tuple[str, str]:
    """phan_con_lai bắt đầu bằng dòng 'Đọc hiểu'. Tìm bộ câu hỏi nằm CUỐI văn bản:
    là 1 dãy mục đánh số liên tục 1,2,3,...N (N = số mục cuối cùng), đứng ở cấp cao nhất.
    Trả về (doc_hieu_text, cau_hoi_text)."""
    lines = phan_con_lai.splitlines()

    # thu thập mục cấp cao nhất: (label, dòng_bắt_đầu)
    items = []
    for i, line in enumerate(lines):
        m = NUM_RE.match(line.strip())
        if m:
            items.append((int(m.group(1)), i))

    if not items:
        return phan_con_lai.strip(), ""

    # đi ngược từ mục cuối cùng, yêu cầu nhãn giảm dần liên tục về 1
    cut_pos = None
    expected = items[-1][0]
    idx = len(items) - 1
    while idx >= 0:
        label, line_idx = items[idx]
        if label != expected:
            break
        cut_pos = line_idx
        if expected == 1:
            break
        expected -= 1
        idx -= 1

    # chỉ chấp nhận nếu dãy tìm được thực sự kết thúc đúng ở nhãn 1
    if cut_pos is None or items[idx][0] != 1:
        return phan_con_lai.strip(), ""

    # cần ít nhất 2 mục mới coi là 1 "bộ" câu hỏi (tránh bắt nhầm 1 mục lẻ)
    so_muc = len(items) - idx
    if so_muc < 2:
        return phan_con_lai.strip(), ""

    doc_hieu_text = "\n".join(lines[:cut_pos]).strip()
    cau_hoi_text = "\n".join(lines[cut_pos:]).strip()
    return doc_hieu_text, cau_hoi_text


# ── Ghép 3 bước lại: xử lý 1 bài hoàn chỉnh ──

def xu_ly_1_bai(ten_bai: str, noi_dung_bai: str, so_bai: str, ten_bai_lon: str, sub_chu_de: str) -> list[str]:
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
        print(f"[CẢNH BÁO] Bài {so_bai} - mục TỰ ĐÁNH GIÁ không tìm được bộ câu hỏi trắc nghiệm — cần kiểm tra thủ công.")

    return parts


# ── Xử lý mục ĐỌC hoàn chỉnh (gộp 4 bước trên) ──

def cut_doc(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    doc_hieu_van_ban_text, thuc_hanh_doc_hieu_text = tach_2_phan_doc(text)

    parts = []

    cac_bai_doc_hieu = tach_cac_bai(doc_hieu_van_ban_text)
    for ten, noi_dung in cac_bai_doc_hieu:
        parts.extend(xu_ly_1_bai(ten, noi_dung, so_bai, ten_bai, "Đọc hiểu văn bản"))

    cac_bai_thuc_hanh = tach_cac_bai(thuc_hanh_doc_hieu_text)
    for ten, noi_dung in cac_bai_thuc_hanh:
        parts.extend(xu_ly_1_bai(ten, noi_dung, so_bai, ten_bai, "Thực hành đọc hiểu"))

    return parts


# ── Các mục lớn khác (giữ như cũ) ─────────────────────────────────────

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


def cut_single(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    header = make_header(so_bai, ten_bai, chu_de)
    return [f"{header}\n{text.strip()}"]


def cut_numbered(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    header = make_header(so_bai, ten_bai, chu_de)
    parts = []
    for label, content in split_numbered(text):
        parts.append(f"{header}\n{label}. {content}")
    return parts


def cut_raw(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    header = make_header(so_bai, ten_bai, chu_de)
    return [f"{header}\n{text.strip()}"]


# ── Xử lý VIẾT / NÓI VÀ NGHE (cấu trúc giống nhau) ────────────────────

LETTER_RE = re.compile(r'^#{0,3}\s*([a-z])[\.\)]\s*(.*)$')
DINH_HUONG_RE = re.compile(r'^#{0,3}\s*\d*[\.\)]?\s*Định hướng\s*$', re.IGNORECASE | re.MULTILINE)
THUC_HANH_RE  = re.compile(r'^#{0,3}\s*\d*[\.\)]?\s*Thực hành\s*$', re.IGNORECASE | re.MULTILINE)

def split_lettered(text: str) -> list[tuple[str, str]]:
    """Tách theo 'a) ...' 'b) ...' cấp cao nhất."""
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


def tach_dinh_huong_thuc_hanh(noi_dung_bai: str) -> tuple[str, str]:
    """Trả về (dinh_huong_text, thuc_hanh_text), mỗi phần bắt đầu từ chính dòng heading."""
    m1 = DINH_HUONG_RE.search(noi_dung_bai)
    m2 = THUC_HANH_RE.search(noi_dung_bai)

    if m1 and m2:
        dinh_huong_text = noi_dung_bai[m1.start():m2.start()].strip()
        thuc_hanh_text = noi_dung_bai[m2.start():].strip()
    elif m1:
        dinh_huong_text = noi_dung_bai[m1.start():].strip()
        thuc_hanh_text = ""
    elif m2:
        dinh_huong_text = ""
        thuc_hanh_text = noi_dung_bai[m2.start():].strip()
    else:
        dinh_huong_text = noi_dung_bai.strip()
        thuc_hanh_text = ""

    return dinh_huong_text, thuc_hanh_text


def xu_ly_1_de_bai(ten_de: str, noi_dung: str, so_bai: str, ten_bai_lon: str, chu_de: str) -> list[str]:
    header = make_header(so_bai, ten_bai_lon, chu_de, sub=f"đề bài {ten_de}")

    dinh_huong_text, thuc_hanh_text = tach_dinh_huong_thuc_hanh(noi_dung)
    parts = []

    for sub_name, sub_text in [("Định hướng", dinh_huong_text), ("Thực hành", thuc_hanh_text)]:
        if not sub_text.strip():
            continue

        lines = sub_text.splitlines()
        first_letter_match = None
        for i, line in enumerate(lines):
            if LETTER_RE.match(line.strip()):
                first_letter_match = i
                break

        # phần trước mục a) đầu tiên (VD dòng "Bài tập(*): ...") giữ làm phần mở đầu
        intro_text = "\n".join(lines[:first_letter_match]).strip() if first_letter_match is not None else sub_text.strip()

        lettered_items = split_lettered(sub_text)
        if not lettered_items:
            parts.append(f"{header}, {sub_name}\n{sub_text.strip()}")
            continue

        for idx, (label, content) in enumerate(lettered_items):
            if idx == 0 and intro_text and intro_text not in content:
                parts.append(f"{header}, {sub_name}\n{intro_text}\n\n{label}) {content}")
            else:
                parts.append(f"{header}, {sub_name}\n{label}) {content}")

    if not parts:
        parts.append(f"{header}\n{noi_dung.strip()}")

    return parts


def cut_viet_hoac_noi_nghe(text: str, so_bai: str, ten_bai: str, chu_de: str) -> list[str]:
    """Dùng chung cho VIẾT và NÓI VÀ NGHE — tách theo đề bài IN HOA trước,
    sau đó mỗi đề bài tách Định hướng/Thực hành, rồi tách mục a) b) c)."""
    cac_de_bai = tach_cac_bai(text)  # tái dùng hàm đã có, nhận diện IN HOA

    if not cac_de_bai:
        header = make_header(so_bai, ten_bai, chu_de)
        return [f"{header}\n{text.strip()}"]

    parts = []
    for ten_de, noi_dung in cac_de_bai:
        parts.extend(xu_ly_1_de_bai(ten_de, noi_dung, so_bai, ten_bai, chu_de))

    return parts

# ── Xử lý TỰ ĐÁNH GIÁ ──────────────────────────────────────────────────

OPTION_RE = re.compile(r'^\s*[A-Da-d][\.\)]\s')

def split_numbered_dot_only(text: str) -> list[tuple[str, str]]:
    """Giống split_numbered nhưng CHỈ tách theo 'N.' (dấu chấm), không tách theo
    'N)' (dấu ngoặc) — vì dạng ngoặc chỉ là ý liệt kê nhỏ bên trong 1 mục lớn."""
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
    
def normalize_circled_numbers(text: str) -> str:
    """Chuyển ①②③... thành '1. ' '2. ' '3. ' để split_numbered nhận diện đồng nhất."""
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and 0x2460 <= ord(stripped[0]) <= 0x2473:  # ①(2460) .. ⑳(2473)
            num = ord(stripped[0]) - 0x2460 + 1
            rest = stripped[1:].strip()
            out.append(f"{num}. {rest}")
        else:
            out.append(line)
    return "\n".join(out)


def tach_mo_ta_va_phan_con_lai(text: str) -> tuple[str, str, str]:
    """mo_ta_text = phần trước mục '2.' đầu tiên (yêu cầu + tên văn bản + mục '1.').
    ten_bai = đoạn sau dấu ':' và trước dấu '(' trong mo_ta_text.
    phan_con_lai_text = từ mục '2.' đầu tiên trở đi."""
    items = _thu_thap_muc_cap_cao(text)

    split_line_idx = None
    for label, line_idx, _ in items:
        if label == 2:
            split_line_idx = line_idx
            break

    if split_line_idx is None:
        return text.strip(), "", ""

    lines = text.splitlines()
    mo_ta_text = "\n".join(lines[:split_line_idx]).strip()
    phan_con_lai_text = "\n".join(lines[split_line_idx:]).strip()

    m = re.search(r':\s*\n?(.*?)\(', mo_ta_text, re.DOTALL)
    ten_bai = m.group(1).strip() if m else ""

    return mo_ta_text, ten_bai, phan_con_lai_text


TOP_LEVEL_DOT_RE = re.compile(r'^(\d+)\.\s+(.*)$')   # chỉ nhận '1.' '2.', KHÔNG nhận '1)' '2)'


def _thu_thap_muc_cap_cao(text: str) -> list[tuple[int, int, str]]:
    """Trả về [(label, dòng_bắt_đầu, nội_dung), ...] cho các mục '1. 2. 3.' cấp cao nhất.
    CHỈ nhận dạng số có dấu chấm (1.), KHÔNG nhận dạng số có dấu ngoặc (1)) vì
    dạng ngoặc chỉ là các ý liệt kê nhỏ bên trong 1 mục, không phải ranh giới mục."""
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


def tach_noi_dung_va_cau_hoi(phan_con_lai_text: str) -> tuple[str, str]:
    """Quét xuôi các mục '1. 2. 3...' cấp cao nhất. Theo dõi dãy tăng dần liên tục
    (1,2,3,4...). Ngay khi nhãn ĐỘT NGỘT giảm về 1 (không tiếp nối số trước) ->
    đó là điểm bắt đầu bộ Câu hỏi. Cắt tại đó."""
    lines = phan_con_lai_text.splitlines()
    items = _thu_thap_muc_cap_cao(phan_con_lai_text)

    if not items:
        return phan_con_lai_text.strip(), ""

    split_line = None
    prev_label = None

    for label, line_idx, _ in items:
        if prev_label is not None and label == 1 and prev_label != 1:
            # đang tăng dần (prev_label > 1) mà đột ngột về lại 1 -> điểm cắt
            split_line = line_idx
            break
        prev_label = label

    if split_line is None:
        return phan_con_lai_text.strip(), ""

    noi_dung_text = "\n".join(lines[:split_line]).strip()
    cau_hoi_text = "\n".join(lines[split_line:]).strip()
    return noi_dung_text, cau_hoi_text


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

    noi_dung_text, cau_hoi_text = tach_noi_dung_va_cau_hoi(phan_con_lai_text)

    if noi_dung_text:
        for label, content in split_numbered_dot_only(noi_dung_text):
            parts.append(f"{header}, Nội dung\n{label}. {content}")

    if cau_hoi_text:
        parts.append(f"{header}, Câu hỏi\n{cau_hoi_text}")   # <-- 1 part duy nhất, KHÔNG có for loop ở đây
    else:
        print(f"[CẢNH BÁO] Bài {so_bai} - mục TỰ ĐÁNH GIÁ không tìm được bộ câu hỏi trắc nghiệm — cần kiểm tra thủ công.")

    return parts


HANDLERS = {
    "YÊU CẦU CẦN ĐẠT": cut_single,
    "KIẾN THỨC NGỮ VĂN": cut_numbered,
    "ĐỌC": cut_doc,
    "THỰC HÀNH TIẾNG VIỆT": cut_numbered,
    "VIẾT": cut_viet_hoac_noi_nghe,
    "NÓI VÀ NGHE": cut_viet_hoac_noi_nghe,
    "TỰ ĐÁNH GIÁ": cut_tu_danh_gia,
    "HƯỚNG DẪN TỰ HỌC": cut_raw,
}


# ── Đọc file, tách mục lớn, chạy pipeline ────────────────────────────

def extract_ten_bai_va_so(full_text: str) -> tuple[str, str]:
    lines = full_text.splitlines()
    muc_keywords = set(MUC_LON_ALL)

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
        r'^#{0,6}\s*(' + "|".join(re.escape(m) for m in MUC_LON_ALL) + r')\s*$',
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


def cut_bai_muc(input_path: Path) -> Path:
    full_text = input_path.read_text(encoding="utf-8")
    so_bai, ten_bai = extract_ten_bai_va_so(full_text)
    muc_dict = split_muc_lon(full_text)

    all_parts = []
    for muc_name in MUC_LON_ALL:
        body = muc_dict.get(muc_name, "").strip()
        if not body:
            continue
        all_parts.extend(HANDLERS[muc_name](body, so_bai, ten_bai, muc_name))

    output_path = input_path.with_name(input_path.stem + "_chunk.md")
    out_lines = []
    for i, p in enumerate(all_parts, start=1):
        out_lines.append(f"<!-- part {i} -->")
        out_lines.append(p)
        out_lines.append("\n---\n")
    output_path.write_text("\n".join(out_lines), encoding="utf-8")

    print(f"✅ Bài {so_bai} - {ten_bai}: {len(all_parts)} part -> {output_path}")
    return output_path


if __name__ == "__main__":
    INPUT = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\bai\canh_dieu_ngu_van_bai_6.md")
    cut_bai_muc(INPUT)