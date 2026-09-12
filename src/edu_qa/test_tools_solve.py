import json, re, os , sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.configs import env_config

from pathlib import Path


RERANK_CANDIDATES = 3


 
path = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\test_tools.md")
 

def load_queries(md_path, max_queries=30):
    queries = []

    with open(md_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            original_query = line
            clean_query = re.sub(r"\(.*?\)", "", line).strip()

            queries.append({
                "original": original_query,
                "clean": clean_query
            })

            if len(queries) >= max_queries:
                break

    return queries

    
# queries = load_queries(path)

# print(f"Found {len(queries)} queries")

# for q in queries:
#     print(q)

def evaluate_queries(retriever, md_path):

    queries = load_queries(md_path)
    out_file = md_path.with_name(f"{md_path.stem}_result.md")

    with open(out_file, "w", encoding="utf-8") as f:

        for i, item in enumerate(queries, 1):

            original_query = item["original"]
            clean_query = item["clean"]

            candidates = retriever.hybrid_search(clean_query)

            reranked = retriever.rerank(
                clean_query,
                candidates,
                top_k=RERANK_CANDIDATES
            )

            f.write(f"Query {i}: {original_query}\n\n")

            for rank, doc in enumerate(reranked, 1):

                f.write(
                    f"----- Top {rank} -----\n"
                    f"metadata:\n"
                    f"{json.dumps(doc.metadata, ensure_ascii=False, indent=2)}\n\n"
                )

            f.write("\n" + "=" * 100 + "\n\n")

    print(f"Saved: {out_file}")


def run(md_path: Path, subject_filter: str):

    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="tools",
        top_k=15
    )

    evaluate_queries(retriever, md_path)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Đánh giá chất lượng truy vấn")
    run(Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\test_tools.md"), "toan")