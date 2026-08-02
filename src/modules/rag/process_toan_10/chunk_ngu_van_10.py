import re
from pathlib import Path

from underthesea import chunk

# ── Config ─────────────────────────────────────────────────────────
SOURCE = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\grade_10_canh_dieu_ngu_van_2.md")
OUTPUT_DIR = SOURCE.parent / "bai"  # đổi nếu muốn lưu chỗ khác
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MUC_LIST = [
    "YÊU CẦU CẦN ĐẠT",
    "KIẾN THỨC NGỮ VĂN",
    "ĐỌC",
    "THỰC HÀNH TIẾNG VIỆT",
    "VIẾT",
    "NÓI VÀ NGHE",
    "TỰ ĐÁNH GIÁ",
    "HƯỚNG DẪN TỰ HỌC",
]

# Regex nhận diện "BÀI X" — cho phép có # markdown phía trước, không phân biệt hoa/thường phần "Bài"
BAI_PATTERN = re.compile(r"^#{0,6}\s*BÀI\s+(\d+)\b.*$", re.MULTILINE | re.IGNORECASE)

# Regex nhận diện mục lớn — match CHÍNH XÁC (in hoa) theo MUC_LIST, cho phép # phía trước
def build_muc_pattern() -> re.Pattern:
    escaped = [re.escape(m) for m in MUC_LIST]
    pattern = r"^#{0,6}\s*(" + "|".join(escaped) + r")\s*$"
    return re.compile(pattern, re.MULTILINE)

MUC_PATTERN = build_muc_pattern()


def split_by_bai(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Trả về (gioi_thieu_text, [(so_bai, noi_dung_bai), ...])"""
    matches = list(BAI_PATTERN.finditer(text))
    if not matches:
        raise ValueError("Không tìm thấy marker 'BÀI X' nào trong file nguồn.")

    gioi_thieu = text[: matches[0].start()].strip()

    bai_blocks = []
    for i, m in enumerate(matches):
        so_bai = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        bai_blocks.append((so_bai, text[start:end].strip()))

    return gioi_thieu, bai_blocks


def split_by_muc(bai_text: str, so_bai: str) -> dict[str, str]:
    """Tách nội dung 1 bài thành dict {tên mục: nội dung}. Log cảnh báo nếu thiếu mục."""
    matches = list(MUC_PATTERN.finditer(bai_text))

    result = {}
    for i, m in enumerate(matches):
        ten_muc = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(bai_text)
        result[ten_muc] = bai_text[start:end].strip()

    missing = [m for m in MUC_LIST if m not in result]
    if missing:
        print(f"[CẢNH BÁO] Bài {so_bai} thiếu mục: {missing}")

    return result


def save_bai_file(so_bai: str, tieu_de_line: str, muc_dict: dict[str, str]) -> Path:
    lines = [f"# BÀI {so_bai}", tieu_de_line.strip(), ""]
    for muc in MUC_LIST:
        if muc in muc_dict:
            lines.append(f"## {muc}")
            lines.append(muc_dict[muc])
            lines.append("")

    out_path = OUTPUT_DIR / f"canh_dieu_ngu_van_bai_{so_bai}.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path



KET_THUC_MARKER = "ÔN TẬP VÀ TỰ ĐÁNH GIÁ CUỐI HỌC KÌ II"

def cat_bo_phan_cuoi(text: str) -> str:
    """Nếu gặp marker kết thúc học kỳ, cắt bỏ toàn bộ từ đó tới hết file."""
    idx = text.find(KET_THUC_MARKER)
    if idx == -1:
        return text
    return text[:idx].rstrip()

def run():
    text = SOURCE.read_text(encoding="utf-8")
    text = cat_bo_phan_cuoi(text)

    gioi_thieu, bai_blocks = split_by_bai(text)

    # lưu giới thiệu sách
    gt_path = OUTPUT_DIR / "gioi_thieu_sach.md"
    gt_path.write_text(gioi_thieu, encoding="utf-8")
    print(f"✅ Đã lưu: {gt_path}")

    for so_bai, bai_text in bai_blocks:
        # dòng đầu bai_text là marker "BÀI X", dòng kế là tên bài
        block_lines = bai_text.splitlines()
        # tieu_de_line = block_lines[1] if len(block_lines) > 1 else ""
        # Thay đoạn lấy tieu_de_line trong hàm run():
        block_lines = bai_text.splitlines()
        non_empty = [l for l in block_lines[1:] if l.strip()]
        tieu_de_line = non_empty[0] if non_empty else ""
        noi_dung_sau_tieu_de = "\n".join(block_lines[block_lines.index(tieu_de_line) + 1:]) if tieu_de_line else "\n".join(block_lines[1:])
        noi_dung_sau_tieu_de = "\n".join(block_lines[2:])

        muc_dict = split_by_muc(noi_dung_sau_tieu_de, so_bai)
        out_path = save_bai_file(so_bai, tieu_de_line, muc_dict)
        print(f"✅ Đã lưu: {out_path}")


if __name__ == "__main__":
    run()



# bây giờ ta đã có cac file là các bài  , ta sẽ xử lý như sau với các mục , chunk sẽ chứa tên mục và chủ đề , ví dụ như mục đó có các mục như 1 2 3 4 thì chunk có tên mục và chủ đề là nội dung của mục a , ví dụ : Bài 5 Thơ văn nguyễn trãi , chủ đề yêu cầu cần đạt
#  - Yêu cầu cần đạt : nó là 1 chunk 
#  - KIẾN THỨC NGỮ VĂN : nó có các mục như : 1. .... 2. .... 3. .. thì tạo các chunk chứ tên bài và chủ đề , sau đó là nội dung , chứa cả  1.....
# nếu mục đó quá dài thì chia nhỏ thành các đoạn nhưng vẫn chứa tên bài và chủ đề , ví dụ : Bài 5 Thơ văn nguyễn trãi , chủ đề yêu cầu cần đạt , sua đó là nọi dung 
# - Đọc : có 2 mục con là Đọc hiểu văn bản và Thực hành đọc hiểu , bốc cục 2 mục đó như sau 
# + Đọc hiểu văn bản 
# ++ Tên bài 
# ++ 1. Chuẩn bị : toàn bô là 1 chunk 
# ++ 2. Đọc hiểu ( có thể không có số 2 nhưng nên lấy theo từ 'Đọc hiểu')
# +++ có thể có các mục con như I , II , 1 ,2,3.. ta sẽ chia các mục đó thành từng phần sau đó chia các phần đo thành các chunk ,nên chunk theo đoạn nhưng không quá dài ,các chunk vẫn giữ tên bài và chủ đề , ví dụ : Bài 5 Thơ văn nguyễn trãi , chủ đề Đọc hiểu văn bản , sau đó là nội dung của mục con đó
# +++ mục câu hỏi : mục này không ghi rõ ràng như mục chuẩn hay Đọc hiểu mà nó là 4 đến 5 câu hỏi dạng như 1. .... 2. ... và đây sẽ là 1 chunk
# lưu ý có nhiều bài chứ không chỉ một bài
# + Thức hành đọc hiểu 
# lưu ý : mục này cấu trúc cũng tương tự như mục Đọc hiểu văn bản nhưng có thể có các mục con khác nhau, chúng ta sẽ chunk theo từng mục con và giữ tên bài và chủ đề
# - Thực hành tiếng việt : có các mục như 1,2,3,4... ta sẽ tách các mục sau sau đó tạo các chunk , nếu mục đó quá dài thì chia nhỏ thành các đoạn nhưng vẫn giữ tên bài và chủ đề
# - VIẾT : 
# + tên bài viết 
# + 1 Định hướng : có các mục như a, b c... ta sẽ tách thành các chunk theo đoạn 
# + 2. Thực hành viết : có các mục như a, b c... ta sẽ tách thành các chunk theo đoạn

## lưu ý ; có 8 mục lớn nhưng ta tạm làm 5 mục trước , viết code sao cho sau này tối ưu và dùng lại nhanh chóng, input là path chứa file.md , output là path input nhưng name file thêm '_chunk;p, ví dụ .....bai_1.md -> bai_1_chunk.md

