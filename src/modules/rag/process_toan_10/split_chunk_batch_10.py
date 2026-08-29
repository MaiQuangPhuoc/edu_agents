import re
import ast
from pathlib import Path

# ==================================================
# CONFIG
# ==================================================

base_path = Path(
    r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk"
)

output_root = Path(
    r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver"
)

subjects = ["toan", "ngu_van", "lich_su"]

BATCH_SIZE = 10


# ==================================================
# PARSE 1 FILE
# ==================================================

def parse_chunks(md_text: str):

    chunk_pattern = (
        r"<!-- chunk \d+ -->\s*\n"
        r"---\n"
        r"(.*?)\n"
        r"---\n"
        r"(.*?)(?=(?:<!-- chunk \d+ -->)|\Z)"
    )

    matches = re.findall(
        chunk_pattern,
        md_text,
        flags=re.DOTALL
    )

    chunks = []

    for metadata_text, content in matches:

        metadata = {}

        for line in metadata_text.splitlines():

            line = line.strip()

            if not line:
                continue

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            metadata[key.strip()] = value.strip()

        chunks.append(
            {
                "metadata": metadata,
                "content": content.strip()
            }
        )

    return chunks


# ==================================================
# SAVE BATCHES
# ==================================================

def save_batches(subject, chunks):

    output_dir = output_root / subject
    output_dir.mkdir(parents=True, exist_ok=True)

    batch_id = 1

    for start in range(0, len(chunks), BATCH_SIZE):

        batch = chunks[start:start + BATCH_SIZE]

        output_file = output_dir / f"{subject}_{batch_id}.md"

        with open(output_file, "w", encoding="utf-8") as f:

            for chunk in batch:

                f.write(
                    str(
                        {
                            "metadata": chunk["metadata"],
                            "content": chunk["content"]
                        }
                    )
                )

                f.write("\n")
                f.write("-" * 50)
                f.write("\n")

        batch_id += 1


# ==================================================
# MAIN
# ==================================================

for subject in subjects:

    input_file = (
        base_path
        / subject
        / f"{subject}_10_all_chunks_final_updated.md"
    )

    if not input_file.exists():
        print(f"Không tìm thấy: {input_file}")
        continue

    print(f"Đang xử lý: {subject}")

    text = input_file.read_text(
        encoding="utf-8"
    )

    chunks = parse_chunks(text)

    print(f"  Số chunk: {len(chunks)}")

    save_batches(
        subject,
        chunks
    )

    print("  Hoàn thành")

print("\nDONE")