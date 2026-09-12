import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv

from src.configs import env_config
from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever


load_dotenv()

TOP_K = 5

LINE_PATTERN = re.compile(r"^\d+\.\s*(?:\((?P<do_kho>[^)]+)\)\s*)?(?P<query>.+?)\s*\|\s*(?P<tool>\S+)\s*$")


def _strip_tool_suffix(name: str) -> str:
    return name[:-5] if name.endswith("_tool") else name


def _load_queries(path: Path) -> list[dict]:
    """Đọc file .md, bỏ qua dòng tiêu đề (#, ##), trả về list dict {so_thu_tu, do_kho, query, tool}.
    Tự cộng offset nếu số thứ tự bị reset về 1 (trường hợp gộp nhiều batch vào 1 file)."""
    items = []
    offset = 0
    last_num = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = LINE_PATTERN.match(line)
        if not match:
            continue
        raw_num = int(line.split(".", 1)[0].strip())
        if raw_num == 1 and last_num > 1:
            offset = last_num
        last_num = raw_num
        so_thu_tu = raw_num + offset

        items.append({
            "so_thu_tu": str(so_thu_tu),
            "do_kho": match.group("do_kho") or "",
            "query": match.group("query").strip(),
            "tool": match.group("tool").strip(),
        })
    return items


def run_test(input_path: Path, result_path: Path):
    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",
        tools_collection_name="tools",
        top_k=10,
    )

    items = _load_queries(input_path)

    output_lines = []
    correct_count = 0
    stats_by_level = defaultdict(lambda: [0, 0])  # {do_kho: [correct, total]}

    for item in items:
        so_thu_tu, do_kho, query_text, expected_tool = item["so_thu_tu"], item["do_kho"], item["query"], item["tool"]

        docs = retriever.hybrid_search_tools(query_text, k=15)
        top_docs = retriever.rerank(query_text, docs, top_k=TOP_K)
        top_tool_names = [d.metadata.get("tool_name", "unknown") for d in top_docs]

        # ── Build context từ top_docs: metadata + content từng chunk ──────
        chunk_blocks = []
        for idx, doc in enumerate(top_docs, start=1):
            meta = doc.metadata or {}
            meta_str = ",".join(f" {k}: {v}" for k, v in meta.items())
            block = (
                f"chunk {idx}:\n"
                f"metadata:\n{meta_str}\n"
                f"content:\n{doc.page_content}"
            )
            chunk_blocks.append(block)

        context = "\n\n---\n\n".join(chunk_blocks)

        is_correct = expected_tool in top_tool_names
        if is_correct:
            correct_count += 1
        if do_kho:
            stats_by_level[do_kho][1] += 1
            if is_correct:
                stats_by_level[do_kho][0] += 1

        expected_display = _strip_tool_suffix(expected_tool)
        do_kho_display = f" [{do_kho}]" if do_kho else ""

        output_lines.append(f"Query {so_thu_tu}{do_kho_display}: {query_text} ({expected_display})")
        output_lines.append("")

        result_marks = []
        for i, tool_name in enumerate(top_tool_names, start=1):
            output_lines.append(f"Tool {i}: {_strip_tool_suffix(tool_name)}")
            result_marks.append("✅" if tool_name == expected_tool else "❌")

        output_lines.append("")
        output_lines.append(f"Result Tool: {' '.join(result_marks)}")
        output_lines.append("-" * 21)
        output_lines.append(context)
        output_lines.append("=" * 21)
        output_lines.append("")

        print(f"Query {so_thu_tu} [{do_kho}]: {'PASS' if is_correct else 'FAIL'} | expected={expected_tool} | top3={top_tool_names}")

    output_lines.append(f"\nTổng kết: {correct_count}/{len(items)} query có tool kỳ vọng nằm trong top-{TOP_K}\n")
    for level, (correct, total) in stats_by_level.items():
        output_lines.append(f"  - {level}: {correct}/{total}")

    result_path.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"\nTổng kết: {correct_count}/{len(items)}")
    for level, (correct, total) in stats_by_level.items():
        print(f"  - {level}: {correct}/{total}")
    print(f"\nĐã lưu kết quả vào: {result_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    batch = sys.argv[1] if len(sys.argv) > 1 else "1"

    input_path = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\test_tools_queries_x5.md")
    result_path = Path(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\test_tools_result_x5_top5.md")

    run_test(input_path, result_path)