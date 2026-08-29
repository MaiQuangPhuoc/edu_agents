import json
from pathlib import Path

BASE_DIR = Path(
    r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver"
)

SUBJECTS = [
    "toan"
    # ,
    # "ngu_van",
    # "lich_su"
]


for subject in SUBJECTS:

    subject_dir = BASE_DIR / subject

    if not subject_dir.exists():
        print(f"[WARNING] Không tìm thấy folder: {subject}")
        continue

    copy_files = sorted(
        [
            f for f in subject_dir.glob("*.md")
            if "copy" in f.name.lower()
        ]
    )

    if not copy_files:
        print(
            f"[WARNING] Folder '{subject}' chưa có file chứa chữ 'copy'"
        )
        continue

    all_questions = []
    question_counter = 1

    for file_path in copy_files:

        print(f"Đọc: {file_path.name}")

        try:
            text = file_path.read_text(
                encoding="utf-8"
            ).strip()

            data = json.loads(text)

            if isinstance(data, list):

                for item in data:

                    item["question_id"] = (
                        f"{subject}_{question_counter:05d}"
                    )

                    item.setdefault("completed", 0)
                    item.setdefault("result", [])

                    all_questions.append(item)

                    question_counter += 1

            else:
                print(
                    f"[WARNING] {file_path.name} không phải JSON Array"
                )

        except Exception as e:
            print(
                f"[ERROR] {file_path.name}: {e}"
            )

    output_file = (
        subject_dir
        / f"dataset_{subject}_eval_retriver.md"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        for i, item in enumerate(all_questions):

            f.write(
                json.dumps(
                    item,
                    ensure_ascii=False,
                    indent=2
                )
            )

            if i < len(all_questions) - 1:
                f.write("\n\n---\n\n")

    print(
        f"[DONE] {subject}: "
        f"{len(all_questions)} câu hỏi -> "
        f"{output_file.name}"
    )

print("\nHoàn thành.")