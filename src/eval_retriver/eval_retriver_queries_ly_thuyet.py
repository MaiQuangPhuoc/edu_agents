import sys
import os
import re
import json
from pathlib import Path

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.configs import env_config


SCORE_THRESHOLD = 0.7
TOP_K = 7
RERANK_CANDIDATES = 15


def load_items(md_path: Path):

    raw = md_path.read_text(
        encoding="utf-8"
    ).strip()

    # ===== TH1: JSON Array =====

    try:

        data = json.loads(raw)

        if isinstance(data, list):

            # [
            #   {...},
            #   {...}
            # ]

            if len(data) > 0 and isinstance(data[0], dict):
                return data

            # [
            #   [{...},{...}]
            # ]

            if len(data) > 0 and isinstance(data[0], list):

                flattened = []

                for sub in data:
                    flattened.extend(sub)

                return flattened

    except Exception:
        pass

    # ===== TH2: object --- object =====

    blocks = re.split(
        r"\n-{3,}\n",
        raw
    )

    items = []

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        block = re.sub(
            r"^```[a-zA-Z]*\s*|\s*```$",
            "",
            block
        )

        obj = json.loads(block)

        if isinstance(obj, list):
            items.extend(obj)
        else:
            items.append(obj)

    return items


def eval_retrieve(
    retriever,
    question,
    subject_filter
):

    candidates = retriever.hybrid_search(
        question
    )

    candidates = [
        d
        for d in candidates
        if d.metadata.get("subject")
        == subject_filter
    ]

    reranked = retriever.rerank(
        question,
        candidates,
        top_k=RERANK_CANDIDATES
    )

    filtered = [
        d
        for d in reranked
        if d.metadata.get(
            "rerank_score",
            0.0
        ) >= SCORE_THRESHOLD
    ]

    filtered = sorted(
        filtered,
        key=lambda x: x.metadata.get(
            "rerank_score",
            0.0
        ),
        reverse=True
    )[:TOP_K]

    return [
        d.metadata.get("chunk_id")
        for d in filtered
    ]


def run(
    md_path: Path,
    subject_filter: str
):

    print("\n" + "=" * 80)
    print(md_path.name)
    print("=" * 80)

    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",
        top_k=15
    )

    items = load_items(md_path)

    print(
        f"Đã load {len(items)} câu hỏi"
    )

    for idx, item in enumerate(
        items,
        start=1
    ):

        try:

            result_ids = eval_retrieve(
                retriever,
                item["question"],
                subject_filter
            )

            item["result"] = result_ids
            item["completed"] = 1

            print(
                f"[{idx}/{len(items)}] "
                f"{item['question_id']}"
            )

        except Exception as e:

            print(
                f"[ERROR] "
                f"{item.get('question_id','unknown')}"
            )

            print(e)

            item["result"] = []
            item["completed"] = 0

    out_path = md_path.with_name(
        md_path.stem
        + "_result_eval_v2_m3.md"
    )

    lines = []

    for item in items:

        lines.append(
            json.dumps(
                item,
                ensure_ascii=False,
                indent=2
            )
        )

    out_path.write_text(
        "\n\n---\n\n".join(lines),
        encoding="utf-8"
    )

    print(
        f"\n✅ Đã ghi: {out_path}"
    )


if __name__ == "__main__":

    INPUTS = [

        (
            Path(
                r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\lich_su\dataset_lich_su_eval_retriver.md"
            ),
            "Lịch sử 10"
        ),

        (
            Path(
                r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\ngu_van\dataset_ngu_van_eval_retriver.md"
            ),
            "Ngữ văn 10"
        ),

        (
            Path(
                r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\toan\dataset_toan_eval_retriver.md"
            ),
            "Toán 10"
        )
    ]

    for input_path, subject in INPUTS:

        run(
            input_path,
            subject
        )

    print("\n🎉 Hoàn thành đánh giá 3 môn")

    print("\n✅ Hoàn thành toàn bộ đánh giá Retriever")

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