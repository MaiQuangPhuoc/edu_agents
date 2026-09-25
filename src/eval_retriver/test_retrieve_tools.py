import sys, os, json ,re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from src.configs import env_config
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.clients.embedding import embeddings_qa
from src.edu_exam import evaluate_exam_v2 as ev   # chỉnh đúng đường dẫn import thật

EXAM_DIR = Path(r'D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\test_exam')


def load_latest_exam() -> list:
    files = sorted(EXAM_DIR.glob("exam_*.json"))
    return json.loads(files[-1].read_text(encoding="utf-8"))


def build_retriever():
    return VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",
        tools_collection_name="tools",
        top_k=10,
    )

def _norm_chapter(s: str) -> str:
    s = (s or "").lower().strip()
    s = re.sub(r"^chương\s*[ivx\d]+\s*[:\-–.]?\s*", "", s)
    return re.sub(r"\s+", " ", s)


def _match(a: str, b: str, chapter: bool = False) -> bool:
    if chapter:
        a, b = _norm_chapter(a), _norm_chapter(b)
    else:
        a, b = (a or "").lower().strip(), (b or "").lower().strip()
    return bool(a and b and (a == b or a in b or b in a))


def filter_tools(docs: list, q: dict) -> tuple[list, str]:
    """Lớp 1: lọc theo chapter_name~chuong. Lớp 2: lọc theo lesson~bai. Rỗng thì giữ kết quả lớp trước."""
    note = []
    ch = [d for d in docs if _match(d.metadata.get("chapter_name", ""), q.get("chuong", ""), chapter=True)]
    if ch:
        docs = ch
    else:
        note.append("chương KHÔNG khớp")
    ls = [d for d in docs if _match(d.metadata.get("lesson", ""), q.get("bai", ""))]
    if ls:
        docs = ls
    else:
        note.append("bài KHÔNG khớp")
    return docs, ", ".join(note)

def main():
    exam = load_latest_exam()
    retriever = build_retriever()

    questions = [q for q in exam if q.get("type", "bai_tap") == "bai_tap"]
    stat = {"total": 0, "no_chapter_match": 0, "no_lesson_match": 0}

    for i, q in enumerate(questions, 1):
        stat["total"] += 1
        question = q["question"]
        print(f"\n===== [{i}] chuong={q.get('chuong')} | bai={q.get('bai')} | dang_bai={q.get('dang_bai')}")
        print(f"  {question}")

        variants = {
            "raw":        question,
            "dang_bai":   q.get("dang_bai", ""),
            "dang_bai+q": f"{q.get('dang_bai', '')}: {question}",
        }
        for name, qry in variants.items():
            docs = retriever.hybrid_search_tools(qry, k=30)      # lấy rộng rồi mới lọc
            before = len(docs)
            docs, note = filter_tools(docs, q)
            reranked = retriever.rerank(qry, docs, top_k=ev.TOOLS_TOP_K)
            scored = [(d.metadata.get("tool_name"), round(d.metadata.get("rerank_score", 0), 3)) for d in reranked]
            print(f"  [{name}] {before}->{len(docs)} docs {('| ⚠ ' + note) if note else ''}\n      {scored}")
            if name == "raw":
                stat["no_chapter_match"] += int("chương" in note)
                stat["no_lesson_match"] += int("bài" in note)

    print("\n===== TỔNG KẾT =====")
    print(stat)


if __name__ == "__main__":
    main()