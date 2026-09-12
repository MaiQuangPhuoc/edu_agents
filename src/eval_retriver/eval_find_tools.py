import re
from collections import Counter

FILE_PATH = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\test_tools_result_x5_top5.md"

# Đọc file
with open(FILE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Lấy toàn bộ Result Tool
matches = re.findall(
    r"Result Tool:\s*(✅|❌)\s*(✅|❌)\s*(✅|❌)\s*(✅|❌)\s*(✅|❌)",
    text
)

# Chuyển thành list dạng:
# ["✅ ❌ ❌ ❌ ❌", "❌ ✅ ❌ ❌ ❌", ...]
result_list = [
    f"{a} {b} {c} {d} {e}"
    for a, b, c, d, e in matches
]

# Đếm
counter = Counter(result_list)

top1 = counter["✅ ❌ ❌ ❌ ❌"]
top2 = counter["❌ ✅ ❌ ❌ ❌"]
top3 = counter["❌ ❌ ✅ ❌ ❌"]
top4 = counter["❌ ❌ ❌ ✅ ❌"]
top5 = counter["❌ ❌ ❌ ❌ ✅"]
miss = counter["❌ ❌ ❌ ❌ ❌"]

hit_top5 = top1 + top2 + top3 + top4 + top5
total = len(result_list)

# In danh sách đã trích xuất
print("=" * 80)
print("LIST RESULT TOOL")
print("=" * 80)

for i, item in enumerate(result_list, start=1):
    print(f"{i:03d}. {item}")

# Thống kê
print("\n")
print("=" * 80)
print("THỐNG KÊ")
print("=" * 80)

print(f"Tổng query                : {total}")
print(f"Top-1 (✅ ❌ ❌ ❌ ❌)           : {top1}")
print(f"Top-2 (❌ ✅ ❌ ❌ ❌)           : {top2}")
print(f"Top-3 (❌ ❌ ✅ ❌ ❌)           : {top3}")
print(f"Top-4 (❌ ❌ ❌ ✅ ❌)           : {top4}")
print(f"Top-5 (❌ ❌ ❌ ❌ ✅)           : {top5}")
print(f"Không trong Top-5         : {miss}")
print(f"Có xuất hiện trong Top-5  : {hit_top5}")

print("\n")
print("=" * 80)
print("TỶ LỆ")
print("=" * 80)

if total > 0:
    print(f"Top-1 Rate : {top1 / total * 100:.2f}%")
    print(f"Top-2 Rate : {top2 / total * 100:.2f}%")
    print(f"Top-3 Rate : {top3 / total * 100:.2f}%")
    print(f"Top-4 Rate : {top4 / total * 100:.2f}%")
    print(f"Top-5 Rate : {top5 / total * 100:.2f}%")
    print(f"Miss Rate  : {miss / total * 100:.2f}%")
    print(f"Hit@5      : {hit_top5 / total * 100:.2f}%")

print("\n")
print("=" * 80)
print("RAW COUNTER")
print("=" * 80)

for k, v in sorted(counter.items()):
    print(f"{k:10s} : {v}")