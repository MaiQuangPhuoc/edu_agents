from dotenv import load_dotenv
load_dotenv()

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.configs import env_config
from src.clients.embedding import embeddings_qa
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.edu_planning.plan_context import sgk_overview_text

# ---- chỉnh ở đây ----
SUBJECT = "Lịch sử 10"
CHAPTERS = ["I", "II", "III", "IV", "V", "VI"]      # chương cần thử
MIN_SCORE = 0.7                                       # ngưỡng giữ chunk sau rerank
# ---------------------

if __name__ == "__main__":
    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_final",
        top_k=10,
    )
    for ch in CHAPTERS:
        out = sgk_overview_text(retriever, {"subject": SUBJECT, "chapters": [ch]}, min_score=MIN_SCORE)
        print("\n=== KẾT QUẢ (đưa vào prompt) ===")
        print(out)
        print("-" * 80)