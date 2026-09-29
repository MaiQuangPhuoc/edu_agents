"""
File: retrieval_rerank_parallel.py
50 queries, batch size = 5 -> 10 batch.

Fan-Out: các BATCH chạy song song (worker=3 -> 3 batch cùng lúc, không tuần tự 1,2,3...)
Fan-In:  gom kết quả theo batch_id, ghi ra theo đúng thứ tự batch.

Fix so với bản gốc (nguyên nhân crash không traceback):
- create_retriever() bị gọi lại mỗi batch -> load embedding model + reranker
  nhiều lần song song -> tốn RAM/VRAM, rất dễ bị OS kill giữa chừng.
  => Sửa: chỉ tạo retriever 1 LẦN DUY NHẤT, dùng chung cho mọi batch/thread.
- Model rerank (sentence-transformers) không thread-safe khi nhiều thread
  gọi đồng thời -> có thể crash native không traceback.
  => Sửa: khoá riêng bước rerank bằng Lock, các batch vẫn chạy song song ở
     bước retrieval (I/O tới Qdrant), chỉ serialize đúng lúc gọi model.
- rerank() cũ gọi batch_size=1 -> mỗi query tốn ~26s vì không tận dụng GPU
  batching, khiến "chạy song song" nhưng thực chất giống hệt tuần tự (vì
  rerank chiếm gần hết thời gian và bị khoá serialize theo từng query).
  => Sửa: gộp cả batch (nhiều query) vào 1 lần gọi rerank_batch() duy nhất
     (xem retrievers2.py) thay vì gọi rerank() riêng cho từng query.
- Log lỗi kèm traceback đầy đủ thay vì chỉ str(e).
"""

import sys
import os
import time
import threading
import traceback

from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
)

from src.configs import env_config
from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever


INPUT_PATH = Path(
    r"D:/VKU/Nam_3/thuc_tap_doanh_nghiep_he_eSTI/EDUAGENT/src/modules/documents/doc_git/books/10/chunk/tools/queries_test_tools_x5_50.md"
)
OUTPUT_PATH = INPUT_PATH.with_name(
    INPUT_PATH.stem + "_1111.md"
)

TOP_K = 5
BATCH_SIZE = 5
MAX_WORKERS = 3
SUBJECT_FILTER = "Toán 10"

# Retriever DUY NHẤT, dùng chung cho mọi batch chạy song song.
_retriever = VectorStoreRetriever(
    url=env_config.qdrant_url,
    api_key=env_config.qdrant_api_key,
    embeddings=embeddings_qa,
    collection_name="doc_final",
    tools_collection_name="tools",
    top_k=10,
)

# Chỉ khoá bước rerank (gọi model) — retrieval vẫn song song giữa các batch.
_rerank_lock = threading.Lock()


def load_queries(path):
    items = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) < 3:
            continue
        items.append({
            "full_line": line,
            "query_text": parts[0].strip(),
            "tool_name": parts[1].strip(),
            "ten_bai": parts[2].strip(),
        })
    return items


def filter_by_subject(docs, subject):
    return [d for d in docs if d.metadata.get("subject") == subject]


def format_chunk_md(rank, doc):
    meta = doc.metadata or {}
    meta_lines = "\n".join(f"  - {k}: {v}" for k, v in meta.items())
    return (
        f"**Chunk {rank}** (rerank_score = {meta.get('rerank_score', 'N/A')})\n\n"
        f"- Metadata:\n{meta_lines}\n\n"
        f"- Content:\n```\n{doc.page_content}\n```\n"
    )


def process_batch(batch_id, batch):
    batch_begin_dt = datetime.now()
    batch_begin = time.perf_counter()
    print(f"\n[BATCH {batch_id}] START {batch_begin_dt.strftime('%H:%M:%S')}")

    # 1) Retrieval cho từng query trong batch (I/O tới Qdrant, khá rẻ -> để tuần tự
    #    trong batch cũng ổn, các batch khác vẫn đang chạy song song ở tầng ngoài).
    queries, docs_list, ok_items, retrieval_errors = [], [], [], {}

    for item in batch:
        idx = item["global_idx"]
        query_text = item["query_text"].split(")", 1)[1].strip()
        print(f"[Batch {batch_id}] Retrieval Query {idx}")
        try:
            docs = _retriever.hybrid_search_tools(query_text, k=15)
            docs = filter_by_subject(docs, SUBJECT_FILTER)
        except Exception:
            err = traceback.format_exc()
            print(f"[Batch {batch_id}] ERROR retrieval Query {idx}:\n{err}")
            retrieval_errors[idx] = err
            docs = []
        queries.append(query_text)
        docs_list.append(docs)
        ok_items.append(item)

    # 2) Rerank GỘP cả batch trong 1 lần gọi predict() -> tận dụng GPU batching thật
    #    sự, thay vì 5 lần gọi nhỏ lẻ. Lock chỉ giữ đúng lúc gọi model.
    with _rerank_lock:
        try:
            top_docs_list = _retriever.rerank_batch(queries, docs_list, top_k=TOP_K)
        except Exception:
            err = traceback.format_exc()
            print(f"[Batch {batch_id}] ERROR rerank_batch:\n{err}")
            top_docs_list = [[] for _ in queries]

    out_parts = []
    for item, top_docs in zip(ok_items, top_docs_list):
        idx = item["global_idx"]

        if idx in retrieval_errors:
            out_parts.append("\n".join([
                f"## Query {idx}",
                f"**Full:** {item['full_line']}",
                "",
                f"_LOI (retrieval):_\n```\n{retrieval_errors[idx]}\n```\n",
            ]))
            continue

        section = [f"## Query {idx}", f"**Full:** {item['full_line']}", ""]
        if not top_docs:
            section.append("_Không tìm được chunk nào._\n")
        else:
            for rank, doc in enumerate(top_docs, start=1):
                section.append(format_chunk_md(rank, doc))
        out_parts.append("\n".join(section))

    batch_elapsed = time.perf_counter() - batch_begin
    batch_end_dt = datetime.now()
    print(f"[BATCH {batch_id}] DONE ({batch_elapsed:.2f}s)")

    content = (
        f"# Batch {batch_id}\n\n"
        f"- Start: {batch_begin_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- End: {batch_end_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- Duration: {batch_elapsed:.2f}s\n\n"
        + "\n\n---\n\n".join(out_parts)
        + "\n\n==================================================\n\n"
    )

    return batch_id, content


def main():
    program_begin_dt = datetime.now()
    program_begin = time.perf_counter()
    print(f"\nSTART: {program_begin_dt.strftime('%Y-%m-%d %H:%M:%S')}")

    items = load_queries(INPUT_PATH)
    print(f"Đọc được {len(items)} query")

    all_batches = []
    batch_id = 1
    for batch_start in range(0, len(items), BATCH_SIZE):
        batch = items[batch_start: batch_start + BATCH_SIZE]
        for offset, item in enumerate(batch):
            item["global_idx"] = batch_start + offset + 1
        all_batches.append((batch_id, batch))
        batch_id += 1

    print(f"Tổng batch: {len(all_batches)}")

    results = {}

    # Fan-out: submit toàn bộ batch, worker=3 -> tối đa 3 batch chạy song song.
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_batch, bid, b): bid for bid, b in all_batches}

        for future in as_completed(futures):
            bid = futures[future]
            try:
                bid, content = future.result()
                results[bid] = content
            except Exception:
                print(f"[ERROR] Batch {bid}:\n{traceback.format_exc()}")
                results[bid] = f"# Batch {bid}\n\n_LOI không xác định, xem log console._\n"

    program_elapsed = time.perf_counter() - program_begin
    program_end_dt = datetime.now()

    # Fan-in: ghi theo đúng thứ tự batch_id.
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for bid in sorted(results.keys()):
            f.write(results[bid])

        f.write(
            "\n\n# SUMMARY\n\n"
            f"- Start: {program_begin_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"- End: {program_end_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"- Duration: {program_elapsed:.2f}s\n"
        )

    print(f"\nEND: {program_end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"TOTAL TIME: {program_elapsed:.2f}s")
    print(f"\nĐã lưu kết quả vào:\n{OUTPUT_PATH}")


if __name__ == "__main__":
    main()