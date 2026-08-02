from pathlib import Path
import shutil

src_dir = Path(r"D:\rikai\thumnail")
dst_dir = Path(r"D:\rikai\thumnail_new")

names = [
    "231.10.42.21.06.001",
    "231.90.43.22.04.001",
    "231.90.39.21.04.001",
    "231.10.39.21.06.001",
    "220.10.41.21.02.001",
    "210.90.42.20.10.001",
    "210.32.42.20.01.001",
    "210.30.42.20.04.001",
    "212.30.44.52.03.001",
    "212.30.44.52.01.001",
    "210.30.42.20.01.002",
    "220.10.40.20.03.001",
    "215.92.46.22.01.002",
    "215.30.44.21.01.001",
    "310.32.42.50.04.001",
    "323.30.40.40.04.001",
    "3210.52",
    "329.30.44.51.01.001",
    "3551.50",
    "331.12.42.51.01.001",
    "2501.43",
    "2582.20",
    "220.10.41.21.01.001",
    "215.30.46.51.99.001",
    "224.30.55.21.01.001",
    "220.12.43.22.03.001",
    "231.10.30.20.06.001",
    "215.30.40.20.01.001",
    "232.32.44.22.03.001",
    "220.10.41.21.06.001",
    "231.10.39.21.03.002",
    "2218.50",
    "3291.50",
    "3336.20",
    "3210.51",
    "3511.81",
    "3506.61",
    "321.93.42.50.13.001",
    "176.009",
    "324.30.38.50.03.001",
]

name_set = set(names)

matched = []
for p in src_dir.iterdir():
    if p.is_file() and p.stem in name_set:
        matched.append(p)

found_names = {p.stem for p in matched}
missing = name_set - found_names

print(f"Số name yêu cầu: {len(name_set)}")
print(f"Số ảnh tương thích tìm thấy: {len(matched)}")
if missing:
    print(f"Không tìm thấy ảnh cho ({len(missing)}):", sorted(missing))

confirm = input("Nhập y để xác nhận copy: ").strip().lower()
if confirm == "y":
    dst_dir.mkdir(parents=True, exist_ok=True)
    for p in matched:
        shutil.copy2(p, dst_dir / p.name)
    print(f"Đã copy {len(matched)} ảnh vào {dst_dir}")
else:
    print("Đã hủy, không copy.")