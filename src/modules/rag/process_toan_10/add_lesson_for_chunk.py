import re
from pathlib import Path

base_path = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk"

subjects = ["toan", "ngu_van", "lich_su"]


def add_sub_type(metadata: str, subject: str) -> str:
    """
    Với lịch sử và ngữ văn:
    nếu chưa có sub_type thì thêm:
    sub_type:
    """

    if subject not in ["ngu_van", "lich_su"]:
        return metadata

    if re.search(r"^sub_type\s*:", metadata, flags=re.MULTILINE):
        return metadata

    lines = metadata.splitlines()

    insert_idx = len(lines)

    for i, line in enumerate(lines):
        if line.startswith("sub_id:"):
            insert_idx = i
            break

    lines.insert(insert_idx, "sub_type: ")

    return "\n".join(lines)


def process_md_file(file_path: Path, subject: str):

    text = file_path.read_text(encoding="utf-8")

    chunk_pattern = r"(<!-- chunk \d+ -->\s*\n---\n.*?)(?=(?:<!-- chunk \d+ -->)|\Z)"

    chunks = re.findall(
        chunk_pattern,
        text,
        flags=re.DOTALL
    )

    processed_chunks = []

    for chunk in chunks:

        match = re.search(
            r"---\n(.*?)\n---\n(.*)",
            chunk,
            flags=re.DOTALL
        )

        if not match:
            processed_chunks.append(chunk)
            continue

        metadata = match.group(1)
        content = match.group(2).strip()

        # ==================================
        # Thêm sub_type cho văn + lịch sử
        # ==================================
        metadata = add_sub_type(
            metadata,
            subject
        )

        # ==================================
        # Lấy lesson giữa lesson: và id_lesson:
        # ==================================
        lesson_match = re.search(
            r"lesson:\s*(.*?)\s*\nid_lesson:",
            metadata,
            flags=re.DOTALL
        )

        lesson = ""

        if lesson_match:
            lesson = lesson_match.group(1).strip()

        # ==================================
        # Thêm lesson vào content
        # ==================================
        if lesson:
            content = f"[ {lesson} ]\n\n{content}"

        new_chunk = (
            chunk[:match.start(1)]
            + metadata
            + "\n---\n"
            + content
        )

        processed_chunks.append(new_chunk)

    return "\n\n".join(processed_chunks)


for mon in subjects:

    input_path = (
        Path(base_path)
        / mon
        / f"{mon}_10_all_chunks_final.md"
    )

    if not input_path.exists():
        print(f"Không tìm thấy: {input_path}")
        continue

    new_text = process_md_file(
        input_path,
        mon
    )

    output_path = input_path.with_name(
        input_path.stem + "_updated.md"
    )

    output_path.write_text(
        new_text,
        encoding="utf-8"
    )

    print(f"Đã xử lý: {output_path}")