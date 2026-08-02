from pathlib import Path

img_dir = Path(r"D:\rikai\thumnail")

names = [p.stem for p in img_dir.iterdir() if p.is_file()]

print(f"Tổng số ảnh: {len(names)}")
for n in sorted(names):
    print(n)