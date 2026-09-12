import re
import json
from pathlib import Path
    from src.edu_qa.retriever.qdrant_retriever import QdrantRetriever
# ==========================================================
# CONFIG
# ==========================================================

TOOLS_TOP_K = 3
SEARCH_K = 15

INPUT_FILE = "../test_tools.md"

# ==========================================================
# RETRIEVE
# ==========================================================

def retrieve_tools(retriever, query: str, top_k: int = TOOLS_TOP_K):
    """
    Hybrid Search -> Rerank -> Top K
    """

    docs = retriever.hybrid_search_tools(
        query=query,
        k=SEARCH_K
    )

    reranked = retriever.rerank(
        query=query,
        docs=docs,
        top_k=top_k
    )

    return reranked


# ==========================================================
# CLEAN QUERY
# ==========================================================

def extract_query(line: str) -> str:
    """
    Input:
        1. Xét tính đúng sai của mệnh đề ... (xet_menh_de)

    Output:
        Xét tính đúng sai của mệnh đề ...
    """

    line = line.strip()

    # bỏ số thứ tự
    line = re.sub(r"^\d+\.\s*", "", line)

    # bỏ phần (tool_name)
    line = re.sub(r"\s*\([^)]*\)\s*$", "", line)

    return line.strip()


# ==========================================================
# MAIN
# ==========================================================

def main(retriever):

    input_path = Path(INPUT_FILE)

    output_path = input_path.with_name(
        f"{input_path.stem}_result.md"
    )

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    queries = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if not re.match(r"^\d+\.", line):
            continue

        query = extract_query(line)

        if query:
            queries.append(query)

    print(f"Found {len(queries)} queries")

    report = []

    report.append("# TOOL RETRIEVAL TEST\n\n")

    for idx, query in enumerate(queries, start=1):

        print(f"[{idx}/{len(queries)}] {query}")

        report.append(f"# Query {idx}\n\n")
        report.append(f"**Query:** {query}\n\n")

        try:

            docs = retrieve_tools(
                retriever=retriever,
                query=query,
                top_k=TOOLS_TOP_K
            )

            if not docs:
                report.append("Không tìm thấy kết quả.\n\n")
                report.append("---\n\n")
                continue

            for rank, doc in enumerate(docs, start=1):

                report.append(f"## Top {rank}\n\n")

                metadata = getattr(doc, "metadata", {})

                if metadata:

                    report.append("### Metadata\n\n")
                    report.append("```json\n")
                    report.append(
                        json.dumps(
                            metadata,
                            ensure_ascii=False,
                            indent=2
                        )
                    )
                    report.append("\n```\n\n")

                content = getattr(doc, "page_content", "")

                report.append("### Content\n\n")
                report.append("```text\n")
                report.append(content)
                report.append("\n```\n\n")

            report.append("---\n\n")

        except Exception as e:

            report.append(
                f"ERROR: {str(e)}\n\n"
            )
            report.append("---\n\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(report)

    print(f"\nSaved: {output_path}")


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    # thay bằng retriever thật của bạn


    retriever = QdrantRetriever()

    main(retriever)