import json
from pathlib import Path

subjects = ["toan", "ngu_van", "lich_su"]
# subjects = ["lich_su"]

OUTPUT_PATH = Path(
    r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\metrix.md"
)

def compute_metrics(gold_chunks, result_chunks):
    metrics = {"hit": [], "recall": []}
    gold = set(gold_chunks)

    for k in [1, 3, 5]:
        top_k = set(result_chunks[:k])

        hit = int(len(gold & top_k) > 0)
        recall = len(gold & top_k) / len(gold) if gold else 0

        metrics["hit"].append(hit)
        metrics["recall"].append(round(recall, 4))

    return metrics


all_reports = []

for subject in subjects:

    dataset_path = Path(
        rf"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\eval\eval_retriver\{subject}\dataset_{subject}_eval_retriver_result_eval.md"
    )

    print(f"\nĐang xử lý: {dataset_path}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        text = f.read()

    data = [
        json.loads(block.strip())
        for block in text.split("---")
        if block.strip()
    ]

    # thêm hit và recall cho từng câu
    for item in data:

        metrics = compute_metrics(
            item.get("gold_chunks", []),
            item.get("result", [])
        )

        item["hit"] = metrics["hit"]
        item["recall"] = metrics["recall"]

    n = len(data)

    summary = {
        "subject": subject,
        "total_questions": n,
        "hit@1": round(sum(x["hit"][0] for x in data) / n, 4),
        "hit@3": round(sum(x["hit"][1] for x in data) / n, 4),
        "hit@5": round(sum(x["hit"][2] for x in data) / n, 4),
        "recall@1": round(sum(x["recall"][0] for x in data) / n, 4),
        "recall@3": round(sum(x["recall"][1] for x in data) / n, 4),
        "recall@5": round(sum(x["recall"][2] for x in data) / n, 4)
    }

    all_reports.append(summary)

    # ghi đè file dataset với hit và recall mới thêm
    with open(dataset_path, "w", encoding="utf-8") as f:

        for i, item in enumerate(data):

            f.write(
                json.dumps(
                    item,
                    ensure_ascii=False,
                    indent=2
                )
            )

            if i < len(data) - 1:
                f.write("\n\n---\n\n")

    print("\n===== RETRIEVER EVALUATION =====")

    for k, v in summary.items():

        if k == "subject":
            print(f"{k}: {v}")

        elif k == "total_questions":
            print(f"{k}: {v}")

        else:
            print(f"{k}: {v:.2%}")

# lưu báo cáo tổng hợp
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:

    for report in all_reports:

        f.write(json.dumps(
            report,
            ensure_ascii=False,
            indent=2
        ))

        f.write("\n\n---\n\n")

print(f"\n[DONE] Saved report: {OUTPUT_PATH}")