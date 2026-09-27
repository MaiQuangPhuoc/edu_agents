"""
File: retrieval_rerank_135.py
Đọc file query (N. (Độ khó) nội dung | tool_name | tên bài),
tách lấy nội dung query bằng split("|"), retrieve + rerank trên collection "doc_final",
lưu top-k chunk (metadata + content) ra file .md cùng path, thêm hậu tố "_result_retrival_tool".
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path

from src.configs import env_config
from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever

INPUT_PATH = Path(r"D:/VKU/Nam_3/thuc_tap_doanh_nghiep_he_eSTI/EDUAGENT/src/modules/documents/doc_git/books/10/chunk/tools/queries_test_tools_x5_50.md")
OUTPUT_PATH = INPUT_PATH.with_name(INPUT_PATH.stem + "_result_retrival_tool_run_song_song.md")


from concurrent.futures import ThreadPoolExecutor, as_completed


TOP_K = 5
BATCH_SIZE = 5

from datetime import datetime
import time 



SUBJECT_FILTER = "Toán 10"
 

def process_query(idx, item, retriever):
    query_text = item["query_text"]
    query_text = query_text.split(')', 1)[1].strip()

    try:
        docs = retriever.hybrid_search_tools(query_text, k=15)
        docs = filter_by_subject(docs, SUBJECT_FILTER)
        top_docs = retriever.rerank(query_text, docs, top_k=TOP_K)

        section = [
            f"## Query {idx}",
            f"**Full:** {item['full_line']}",
            ""
        ]

        if not top_docs:
            section.append("_Không tìm được chunk nào._\n")
        else:
            for rank, doc in enumerate(top_docs, start=1):
                section.append(format_chunk_md(rank, doc))

        return idx, "\n".join(section)

    except Exception as e:
        return idx, "\n".join([
            f"## Query {idx}",
            f"**Full:** {item['full_line']}",
            "",
            f"_LOI: {e}_\n"
        ])
 
def filter_by_subject(docs: list, subject: str) -> list:
    """Chỉ giữ chunk có metadata['subject'] == subject."""
    return [d for d in docs if d.metadata.get("subject") == subject]
 
 
def load_queries(path: Path) -> list[dict]:
    """Mỗi dòng: 'N. (Độ khó) nội dung | tool_name | tên bài' -> tách bằng split('|')."""
    items = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) < 3:
            continue
        query_text = parts[0].strip()
        tool_name = parts[1].strip()
        ten_bai = parts[2].strip()
        items.append({
            "full_line": line,
            "query_text": query_text,
            "tool_name": tool_name,
            "ten_bai": ten_bai,
        })
    return items
 
 
def format_chunk_md(rank: int, doc) -> str:
    meta = doc.metadata or {}
    meta_lines = "\n".join(f"  - {k}: {v}" for k, v in meta.items())
    return (
        f"**Chunk {rank}** (rerank_score = {meta.get('rerank_score', 'N/A')})\n\n"
        f"- Metadata:\n{meta_lines}\n\n"
        f"- Content:\n```\n{doc.page_content}\n```\n"
    )
 
 
 
 
def main():

    # =========================
    # Program start
    # =========================
    program_begin_dt = datetime.now()
    program_begin = time.perf_counter()

    print(
        f"\nSTART: {program_begin_dt.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    items = load_queries(INPUT_PATH)
    print(f"Đọc được {len(items)} query từ {INPUT_PATH}")

    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",
        tools_collection_name="tools",
        top_k=10,
    )

    # Xóa file cũ
    OUTPUT_PATH.write_text("", encoding="utf-8")

    # =========================
    # Process batches
    # =========================
    for batch_start in range(0, len(items), BATCH_SIZE):

        batch_begin_dt = datetime.now()
        batch_begin = time.perf_counter()

        batch = items[batch_start:batch_start + BATCH_SIZE]

        print(
            f"\n=== Batch {batch_start + 1}-{batch_start + len(batch)}/{len(items)} "
            f"| Start: {batch_begin_dt.strftime('%H:%M:%S')} ==="
        )

        out_parts = [None] * len(batch)

        with ThreadPoolExecutor(max_workers=3) as executor:

            futures = {
                executor.submit(
                    process_query,
                    batch_start + offset + 1,
                    item,
                    retriever
                ): offset
                for offset, item in enumerate(batch)
            }

            for future in as_completed(futures):

                offset = futures[future]

                try:
                    idx, result = future.result()

                    out_parts[offset] = result

                    print(
                        f"[DONE] Query {idx}/{len(items)}"
                    )

                except Exception as e:
                    print(
                        f"[ERROR] Query {batch_start + offset + 1}: {e}"
                    )

        # =========================
        # Batch finished
        # =========================
        batch_end_dt = datetime.now()
        batch_elapsed = time.perf_counter() - batch_begin

        print(
            f"=== Batch {batch_start + 1}-{batch_start + len(batch)}/{len(items)} "
            f"| End: {batch_end_dt.strftime('%H:%M:%S')} "
            f"| ({batch_elapsed:.2f}s) ==="
        )

        batch_header = (
            f"# Batch {batch_start + 1}-{batch_start + len(batch)}\n\n"
            f"- Start: {batch_begin_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"- End: {batch_end_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"- Duration: {batch_elapsed:.2f}s\n\n"
        )

        with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
            f.write(batch_header)

            f.write(
                "\n\n---\n\n".join(
                    part for part in out_parts if part is not None
                )
            )

            f.write(
                "\n\n==================================================\n\n"
            )

    # =========================
    # Program end
    # =========================
    program_end_dt = datetime.now()
    program_elapsed = time.perf_counter() - program_begin

    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        f.write(
            "\n\n# SUMMARY\n\n"
            f"- Start: {program_begin_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"- End: {program_end_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"- Duration: {program_elapsed:.2f}s\n"
        )

    print(
        f"\nEND: {program_end_dt.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(
        f"TOTAL TIME: {program_elapsed:.2f}s"
    )

    print(
        f"\nĐã lưu kết quả vào {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
