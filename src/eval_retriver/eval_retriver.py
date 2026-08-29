import sys, os, re, json
from pathlib import Path
import psutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.configs import env_config

SCORE_THRESHOLD = 0.7
TOP_K = 7
RERANK_CANDIDATES = 15
# SUBJECT_FILTER = "Lịch sử 10" 
# SUBJECT_FILTER = "Ngữ văn 10"
# SUBJECT_FILTER = "Toán 10"




def load_items(md_path: Path) -> list[dict]:
    """Tách file .md theo dấu '---' thành từng block JSON, parse ra list dict."""
    raw = md_path.read_text(encoding="utf-8")
    blocks = re.split(r'\n-{3,}\n', raw.strip())
    items = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        # bỏ ```markdown / ``` nếu có
        b = re.sub(r'^```[a-zA-Z]*\s*|\s*```$', '', b.strip())
        items.append(json.loads(b))
    return items


def eval_retrieve(retriever: VectorStoreRetriever, question: str) -> list[str]:
    """Retrieve + rerank, lọc score >= 0.7, lấy top 3 chunk_id."""
    candidates = retriever.hybrid_search(question)

    print(f"\nsau retrieve -- len : {len(candidates)}")
    for d in candidates:
        print("metadata")
        print(d.metadata)
        print("-----")

    # lọc theo môn học
    candidates = [d for d in candidates if d.metadata.get("subject") == SUBJECT_FILTER]

    print(f"\nsau lọc theo môn ---- len : {len(candidates)}")
    for d in candidates:
        print("metadata")
        print(d.metadata)
        print("-----")

    reranked = retriever.rerank(question, candidates, top_k=RERANK_CANDIDATES)

    # print(f"\nsau rerank -- len : {len(reranked)}")
    # for d in reranked:
    #     print("metadata")
    #     print(d.metadata)
    #     print("-----")

    filtered = [d for d in reranked if d.metadata.get("rerank_score", 0.0) >= SCORE_THRESHOLD]
    filtered = sorted(filtered, key=lambda d: d.metadata.get("rerank_score", 0.0), reverse=True)[:TOP_K]

    print(f"\nsau filtered -- len : {len(filtered)}")
    for d in filtered:
        print("metadata")
        print(d.metadata)
        print("-----")

    return [d.metadata.get("chunk_id") for d in filtered]


def run(md_path: Path):
    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",
        top_k=15,
    )

    items = load_items(md_path)
    print(f"Đã load {len(items)} câu hỏi từ {md_path}")

    for item in items:
        result_ids = eval_retrieve(retriever, item["question"])
        item["result"] = result_ids
        item["completed"] = 1
        print(f"[{item['question_id']}] gold={item['gold_chunks']} -> result={result_ids}")

    out_path = md_path.with_name(md_path.stem + "_result_eval.md")
    lines = []
    for item in items:
        lines.append(json.dumps(item, ensure_ascii=False, indent=2))
    out_path.write_text("\n\n---\n\n".join(lines), encoding="utf-8")

    print(f"✅ Ghi kết quả: {out_path}")


# if __name__ == "__main__":
#     INPUT = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\lich_su\dataset_lich_su_eval_retriver.md") 
#     # INPUT = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\ngu_van\dataset_ngu_van_eval_retriver.md")  
#     # INPUT = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\toan\dataset_toan_eval_retriver.md")  

#     run(INPUT)

    # print("cutt")
    # # Chrome
    # os.system("taskkill /F /IM chrome.exe")

    # # Edge
    # os.system("taskkill /F /IM msedge.exe")

    # # Zalo
    # os.system("taskkill /F /IM Zalo.exe")

    # # VS Code
    # os.system("taskkill /F /IM Code.exe")

    # os.system("shutdown /s /t 300")



if __name__ == "__main__":

    INPUTS = [
        Path(
            r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\lich_su\dataset_lich_su_eval_retriver.md"
        ),
        Path(
            r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\ngu_van\dataset_ngu_van_eval_retriver.md"
        ),
        Path(
            r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\toan\dataset_toan_eval_retriver.md"
        )
    ]

    for input_path in INPUTS:

        print("\n" + "=" * 80)
        print(f"ĐANG XỬ LÝ: {input_path.name}")
        print("=" * 80)

        run(input_path)

    print("\n✅ Hoàn thành toàn bộ đánh giá Retriever")if __name__ == "__main__":

    INPUTS = [
        Path(
            r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\lich_su\dataset_lich_su_eval_retriver.md"
        ),
        Path(
            r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\ngu_van\dataset_ngu_van_eval_retriver.md"
        ),
        Path(
            r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\toan\dataset_toan_eval_retriver.md"
        )
    ]

    for input_path in INPUTS:

        print("\n" + "=" * 80)
        print(f"ĐANG XỬ LÝ: {input_path.name}")
        print("=" * 80)

        run(input_path)

    print("\n✅ Hoàn thành toàn bộ đánh giá Retriever")