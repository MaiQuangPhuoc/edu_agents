import json
from pathlib import Path

INPUT_DIR = Path(
    r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\toan"
)

copy_files = sorted(
    [
        f
        for f in INPUT_DIR.glob("*.md")
        if "copy" in f.name.lower()
    ]
)

if not copy_files:
    print("[WARNING] Không tìm thấy file nào chứa 'copy'")
else:
    print(f"Tìm thấy {len(copy_files)} file.")

for file_path in copy_files:

    try:
        print(f"Đang xử lý: {file_path.name}")

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            print(f"[WARNING] File rỗng: {file_path.name}")
            continue

        data = json.loads(text)

        pretty_json = json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )

        file_path.write_text(
            pretty_json,
            encoding="utf-8"
        )

        print(f"[DONE] {file_path.name}")

    except json.JSONDecodeError as e:
        print(
            f"[ERROR] JSON không hợp lệ trong "
            f"{file_path.name}: {e}"
        )

    except Exception as e:
        print(
            f"[ERROR] {file_path.name}: {e}"
        )

print("\nHoàn thành.")