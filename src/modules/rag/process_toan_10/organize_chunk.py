from pathlib import Path

import re
import json
import sys , os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..","..","..")))
from src.modules.rag.vectorstores2 import VectorStoreManager
from langchain_core.documents import Document
from docx import Document
from src.clients.embedding import embeddings_qa
from src.configs import env_config




# văn 
def convert_chunks(input_path):
    input_path = Path(input_path)

    output_path = input_path.with_name(
        f"{input_path.stem}_ver1{input_path.suffix}"
    )

    text = input_path.read_text(encoding="utf-8")

    chunks = text.split("<!-- chunk ")

    new_chunks = []

    for chunk in chunks:
        if not chunk.strip():
            continue

        chunk_id, chunk = chunk.split("-->", 1)
        chunk_id = chunk_id.strip()

        metadata, content = chunk.split("---", 2)[1:]

        data = {}

        for line in metadata.strip().splitlines():
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()

        mon = data["mon"]
        bai = data["bai"]
        id_bai = data["id_bai"]
        muc = data["muc"]
        loai = data["loai"]

        # Bỏ "Môn Ngữ văn 10, "
        section_name = muc.replace(f"Môn {mon}, ", "", 1)

        new_chunk = f"""<!-- chunk {chunk_id} -->
---
type: {loai}
subject: {mon}
chapter_id: {id_bai}
chapter_name: {bai}
lesson: {bai}
id_lesson: {id_bai}
section_id: "{chunk_id}"
section_name: {section_name}
sub_id: ""
sub_name: ""
has_table: false
---
{content.strip()}
"""

        new_chunks.append(new_chunk)

    output_path.write_text(
        "\n\n".join(new_chunks),
        encoding="utf-8"
    )

    print(f"Đã xử lý {len(new_chunks)} chunks")
    print(f"Đã lưu: {output_path}")

# lich su
def convert_history_chunks(input_path):
    input_path = Path(input_path)

    output_path = input_path.with_name(
        f"{input_path.stem}_ver1{input_path.suffix}"
    )

    text = input_path.read_text(encoding="utf-8")

    chunks = text.split("<!-- chunk ")

    new_chunks = []

    for chunk in chunks:
        if not chunk.strip():
            continue

        chunk_id, chunk = chunk.split("-->", 1)
        chunk_id = chunk_id.strip()

        metadata, content = chunk.split("---", 2)[1:]

        data = {}

        for line in metadata.strip().splitlines():
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()

        mon = data.get("mon", "")
        chu_de = data.get("chu_de", "")
        id_chu_de = data.get("id_chu_de", "")
        bai = data.get("bai", "")
        id_bai = data.get("id_bai", "")
        muc = data.get("muc", "")
        noi_dung = data.get("noi_dung", "")
        loai = data.get("loai", "")
        has_table = data.get("has_table", "false")

        new_chunk = f"""<!-- chunk {chunk_id} -->
---
type: {loai}
subject: {mon}
chapter_id: {id_chu_de}
chapter_name: {chu_de}
lesson: {bai}
id_lesson: {id_bai}
section_id: "{chunk_id}"
section_name: {muc}
sub_id: " "
sub_name: {noi_dung}
has_table: {has_table}
---
{content.strip()}
"""

        new_chunks.append(new_chunk)

    output_path.write_text(
        "\n\n".join(new_chunks),
        encoding="utf-8"
    )

    print(f"Đã xử lý: {len(new_chunks)} chunks")
    print(f"Đã lưu: {output_path}")
# =========================
# INPUT FILE .MD
# =========================

from pathlib import Path


def build_history_chunks(file_path):

    text = Path(file_path).read_text(encoding="utf-8")

    text = re.sub(r'<!-- chunk\s+(\d+).*?-->', r'<!-- chunk \1 -->', text)

    all_chunks = []

    for raw_chunk in text.split("<!-- chunk ")[1:]:

        chunk_id = raw_chunk.split("-->")[0].strip()

        metadata_raw, content = raw_chunk.split("---")[1:3]
        # print("-"*30)
        # print(metadata_raw)

        meta = {}

        for line in metadata_raw.splitlines():

            line = line.strip()

            if not line:
                continue

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            meta[key.strip()] = value.strip()

        # print(meta)

        # chunk = {
        #     "metadata": {
        #         "type": meta.get("type", ""),
        #         "subject": meta.get("subject", ""),
        #         "chapter_id": meta.get("chapter_id", ""),
        #         "chapter_name": meta.get("chapter_name", ""),
        #         "lesson": meta.get("lesson", ""),
        #         "id_lesson": meta.get("id_lesson", ""),
        #         "section_id": meta.get("section_id", ""),
        #         "section_name": meta.get("section_name", ""),
        #         "sub_id": meta.get("sub_id", " "),
        #         "sub_name": meta.get("sub_name", ""),
        #         "has_table": meta.get("has_table", False),
        #         "sub_type": " ",
        #         "chunk_id": meta.get("chunk_id", ""),

        #     },
        #     "content": content.strip()
        # }

        all_chunks.append({
            "metadata": meta,
            "content": content.strip()
        })

    return all_chunks


# ------ push Qdrant --------------------------



from langchain_core.documents import Document
import time


def upload_file_to_qdrant(input_path, embeddings_qa):

    all_chunks = build_history_chunks(input_path)

    documents = [
        Document(
            page_content=chunk["content"],
            metadata=chunk["metadata"]
        )
        for chunk in all_chunks
    ]

    print("-" * 40)
    print(f"Documents: {len(documents)}")

    vector_manager = VectorStoreManager(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key
    )

    BATCH_SIZE = 10

    batches = [
        documents[i:i + BATCH_SIZE]
        for i in range(0, len(documents), BATCH_SIZE)
    ]

    for i, batch in enumerate(batches):

        for attempt in range(3):

            try:

                vector_manager.create_vector_store(
                    documents=batch,
                    embeddings=embeddings_qa,
                    collection_name="new_documents"
                )

                print(
                    f"✓ Batch {i+1}/{len(batches)}"
                )

                time.sleep(1)

                break

            except Exception as e:

                print(
                    f"Batch {i+1} lần {attempt+1} lỗi: {e}"
                )

                time.sleep(3)

    print(
        f"✓ Upload xong {len(documents)} chunks"
    )



# tạo file chứa tất cả chunk 
def write_chunks_to_file(all_chunks, output_path):
    lines = []

    for i, chunk in enumerate(all_chunks, start=1):
        meta = chunk["metadata"]
        content = chunk["content"]

        lines.append(f"<!-- chunk {i} -->")
        lines.append("---")
        for key, value in meta.items():
            lines.append(f"{key}: {value}")
        lines.append("---")
        lines.append(content)
        lines.append("")  # dòng trống ngăn cách các chunk

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"Đã ghi {len(all_chunks)} chunk vào {output_path}")


# ------------------ run -----------------------

# input_path = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\ngu_van\canh_dieu_ngu_van_bai_8_chunk_final.md"

# convert_chunks(input_path)

# input_path = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\lich_su\grade_10_canh_dieu_lich_su_chu_de_1_chunk_final_ver1.md"

# convert_history_chunks(input_path)



# path_origin = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\ngu_van"

# input_path = path_origin + r"\canh_dieu_ngu_van_bai_5_chunk_final_ver1.md"

# ------------------------------------------------- thêm id và gom vào 1 file.md  -------------------------------------------

# path_origin = Path(
#     r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\toan"
# )

# all_chunks = []

# # văn + lịch sử 
# # for i in range(5, 9):
# #     input_path = path_origin / f"canh_dieu_ngu_van_bai_{i}_chunk_final_ver1.md"
# #     chunks = build_history_chunks(input_path)
# #     all_chunks.extend(chunks)


# # toán 
# input_path = path_origin / f"toan_10_chunk_final_ver1.md"
# chunks = build_history_chunks(input_path)
# all_chunks.extend(chunks)


# # gán chunk_id tuần tự ls_1 -> ls_n trên toàn bộ chunk đã gộp
# for idx, chunk in enumerate(all_chunks, start=1):
#     chunk["metadata"]["chunk_id"] = f"toan_{idx}"

# print(f"Tổng số chunk: {len(all_chunks)}\n\n")

# write_chunks_to_file(all_chunks, path_origin / "toan_10_all_chunks_final.md")

# for chunk in all_chunks[:10]:
#     print(chunk)
#     print("-" * 100)



# ---- up 1 file.md lên qdrant  ---- 

# path_origin = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\xxx"

# input_path = path_origin + r"\xxx_10_all_chunks_final.md"

# upload_file_to_qdrant(input_path, embeddings_qa)


# ---- up 3 file.md lên qdrant ----

base_path = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk"

subjects = ["toan", "ngu_van", "lich_su"]

for mon in subjects:
    input_path = Path(base_path) / mon / f"{mon}_10_all_chunks_final.md"
    print(f"Uploading: {input_path}")
    upload_file_to_qdrant(input_path, embeddings_qa)
