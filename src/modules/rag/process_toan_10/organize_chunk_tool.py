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
import time


def build_history_chunks(file_path):

    text = Path(file_path).read_text(encoding="utf-8")

    text = re.sub(r'<!-- tool\s+(\d+).*?-->', r'<!-- tool \1 -->', text)

    all_chunks = []

    for raw_chunk in text.split("<!-- tool ")[1:]:

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

        all_chunks.append({
            "metadata": meta,
            "content": content.strip()
        })

    return all_chunks


# ------ push Qdrant --------------------------





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
                    collection_name="tools"
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



base_path = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\tool.md"


input_path = Path(base_path)
print(f"Uploading: {input_path}")
upload_file_to_qdrant(input_path, embeddings_qa)
