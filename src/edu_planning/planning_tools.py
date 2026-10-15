from typing import Optional
from langchain_core.tools import tool
import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.edu_qa.tools.web_search_tool import web_search_edu
from src.edu_qa.tools.tools_search_media import search_youtube_lecture
FETCH_K = 40


def make_planning_tools(retriever, llm_client=None):
    def _filter(docs, chapter_id, lesson):
        if chapter_id:
            docs = [d for d in docs if d.metadata.get("chapter_id") == chapter_id]
        if lesson:
            docs = [d for d in docs if lesson.lower() in d.metadata.get("lesson", "").lower()]
        return docs

    def _fmt(docs):
        out = []
        for d in docs:
            item = {
                "chapter_id": d.metadata.get("chapter_id"),
                "lesson":     d.metadata.get("lesson"),
                "content":    d.page_content[:400],
            }
            if "rerank_score" in d.metadata:
                item["rerank_score"] = round(d.metadata["rerank_score"], 3)
            out.append(item)
        return out

    @tool
    def search_documents(query: str, subject: str, chapter_id: Optional[str] = None,
                         lesson: Optional[str] = None, top_k: int = 5) -> list[dict]:
        """Tìm nhanh tài liệu SGK (hybrid search), KHÔNG xếp hạng lại.

        Dùng khi:
        - Quét rộng xem chương/bài có những nội dung gì.
        - Tra nhanh, chưa cần độ chính xác cao.

        Kết quả không có điểm; thứ tự chỉ mang tính tham khảo.
        Nếu trả rỗng: bỏ chapter_id/lesson hoặc đổi từ khóa.

        Args:
            query: từ khóa/câu cần tìm.
            subject: "Toán 10" | "Ngữ văn 10" | "Lịch sử 10".
            chapter_id: số chương, ví dụ "3" (tùy chọn).
            lesson: tên bài (tùy chọn).
            top_k: số kết quả tối đa.
        """
        docs = retriever.hybrid_search_qa(query, k=FETCH_K, subject=subject)
        return _fmt(_filter(docs, chapter_id, lesson)[:top_k])

    @tool
    def search_documents_reranked(query: str, subject: str, chapter_id: Optional[str] = None,
                                  lesson: Optional[str] = None, top_k: int = 3) -> list[dict]:
        """Tìm tài liệu SGK rồi xếp hạng lại bằng reranker (chính xác hơn, chậm hơn).

        Dùng khi:
        - Cần đoạn tài liệu chính xác làm căn cứ cho quyết định xếp thứ tự/chiến lược.
        - Đã quét rộng và cần chọn đoạn liên quan nhất.

        rerank_score >= 0.6: liên quan rõ; 0.4-0.6: tạm dùng; < 0.4: nên coi là không liên quan.
        Không so điểm này với kết quả của search_documents.

        Args:
            query: từ khóa/câu cần tìm.
            subject: "Toán 10" | "Ngữ văn 10" | "Lịch sử 10".
            chapter_id: số chương, ví dụ "3" (tùy chọn).
            lesson: tên bài (tùy chọn).
            top_k: số kết quả sau rerank.
        """
        docs = _filter(retriever.hybrid_search_qa(query, k=FETCH_K, subject=subject), chapter_id, lesson)
        return _fmt(retriever.rerank(query, docs, top_k=top_k))

    @tool
    def search_web_documents(query: str, subject: str, top_k: int = 3) -> list[dict]:
        """Tìm tài liệu học tập trên web (trang giáo dục uy tín: đề cương, bài giảng, bài tập).

        Dùng khi:
        - Cần gợi ý tài liệu tham khảo cho một giai đoạn/chương trọng tâm.
        Chỉ dùng khi học sinh có dùng tài liệu (so_thich_hoc.dung_tai_lieu khác False).
        Mỗi lần tra một chương hoặc một ý.

        Args:
            query: từ khóa, nên có tên chương/bài.
            subject: "Toán 10" | "Ngữ văn 10" | "Lịch sử 10".
            top_k: số kết quả tối đa.
        """
        res = web_search_edu.func(query=query, subject=subject, max_results=top_k)
        return [{"loai": "tai_lieu", "tieu_de": r["title"], "url": r["url"], "tom_tat": r["content"][:300]}
                for r in res]

    @tool
    def search_videos(query: str, subject: str, top_k: int = 2) -> list[dict]:
        """Tìm video bài giảng trên YouTube (chỉ lấy video dài, đã lọc theo tiêu đề liên quan).

        Dùng khi:
        - Cần gợi ý video học cho một giai đoạn/chương trọng tâm.
        Chỉ dùng khi học sinh có dùng video (so_thich_hoc.dung_video là True hoặc học sinh nêu rõ).
        Mỗi lần tra một chương hoặc một ý.

        Args:
            query: từ khóa, nên có tên chương/bài.
            subject: "Toán 10" | "Ngữ văn 10" | "Lịch sử 10".
            top_k: số video tối đa.
        """
        res = search_youtube_lecture.func(query=f"{subject} {query}", llm_client=llm_client, max_results=top_k)
        if res and "error" in res[0]:
            return [{"loi": "Không tra được video lúc này"}]
        return [{"loai": "video", "tieu_de": r["title"], "url": r["url"], "kenh": r["channel"]} for r in res]

    return [search_documents, search_documents_reranked, search_web_documents, search_videos]