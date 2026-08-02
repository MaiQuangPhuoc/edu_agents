from pathlib import Path
import re

INPUT = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\bai\canh_dieu_ngu_van_bai_5.md")

full_text = INPUT.read_text(encoding="utf-8")
print("1. Độ dài file gốc:", len(full_text), "ký tự")

MUC_LON_ALL = [
    "YÊU CẦU CẦN ĐẠT", "KIẾN THỨC NGỮ VĂN", "ĐỌC", "THỰC HÀNH TIẾNG VIỆT",
    "VIẾT", "NÓI VÀ NGHE", "TỰ ĐÁNH GIÁ", "HƯỚNG DẪN TỰ HỌC",
]

pattern = re.compile(
    r'^#{0,6}\s*(' + "|".join(re.escape(m) for m in MUC_LON_ALL) + r')\s*$',
    re.MULTILINE
)
matches = list(pattern.finditer(full_text))
print("2. Số mục lớn tìm thấy:", len(matches))
for m in matches:
    print("   ->", repr(m.group(0)), "tại vị trí", m.start())

# kiểm tra output path có ghi được không
OUTPUT = INPUT.with_name(INPUT.stem + "_chunk.md")
print("3. Output path:", OUTPUT)
print("4. Output path tồn tại?", OUTPUT.exists())
if OUTPUT.exists():
    print("5. Size file output hiện tại:", OUTPUT.stat().st_size, "bytes")