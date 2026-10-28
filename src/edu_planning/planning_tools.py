from typing import Optional
from langchain_core.tools import tool
import json, sys, os , re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.edu_planning.chapter_utils import normalize_chapter_id
from src.edu_qa.tools.web_search_tool import web_search_edu
from src.edu_qa.tools.tools_search_media import search_youtube_lecture
import math

FETCH_K = 40


_PAGES = re.compile(r"(\d{1,4})\s*trang", re.I)
_DATE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")

def _doc_item(r: dict) -> dict:
    txt = f"{r['title']} {r['content']}"
    m, d = _PAGES.search(txt), _DATE.search(txt)
    return {"loai": "tai_lieu", "tieu_de": r["title"], "url": r["url"],
            "so_trang": int(m.group(1)) if m else None, "ngay": d.group(0) if d else None,"mo_ta": r.get("content", "")[:300]}

def _nonempty(res):
    return res or [{"thong_bao": "Không có kết quả phù hợp; hãy đổi từ khóa hoặc bỏ chapter_id/lesson."}]

def make_planning_tools(retriever, llm_client=None):

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
    def search_documents(query: str, subject: str, chapter_id: Optional[str] = None, top_k: int = 5) -> list[dict]:
        """Tìm nhanh tài liệu SGK (hybrid search), KHÔNG xếp hạng lại.

        Dùng để quét xem chương có nội dung gì. Nếu trả rỗng: bỏ chapter_id hoặc đổi từ khóa.

        Args:
            query: từ khóa ngắn (tên khái niệm), không chép nguyên tên bài.
            subject: "Toán 10" | "Ngữ văn 10" | "Lịch sử 10".
            chapter_id: số chương, "I" (Toán) hoặc "5" (Ngữ văn, Lịch sử).
            top_k: số kết quả tối đa.
        """
        chapter_id = (normalize_chapter_id(subject, chapter_id) or chapter_id) if chapter_id else None
        return _nonempty(_fmt(retriever.search_sgk(query, subject, chapter_id, k=top_k)))

    @tool
    def search_documents_reranked(query: str, subject: str, chapter_id: Optional[str] = None, top_k: int = 3) -> list[dict]:
        """Tìm tài liệu SGK rồi xếp hạng lại bằng reranker (chính xác hơn, chậm hơn).

        rerank_score từ 0 đến 1: >= 0.6 liên quan rõ; 0.4-0.6 tạm dùng; < 0.4 coi là không liên quan.

        Args:
            query: từ khóa ngắn (tên khái niệm).
            subject: "Toán 10" | "Ngữ văn 10" | "Lịch sử 10".
            chapter_id: số chương, "I" (Toán) hoặc "5" (Ngữ văn, Lịch sử).
            top_k: số kết quả sau rerank.
        """
        chapter_id = (normalize_chapter_id(subject, chapter_id) or chapter_id) if chapter_id else None
        docs = retriever.search_sgk(query, subject, chapter_id, k=FETCH_K)
        return _nonempty(_fmt(retriever.rerank(query, docs, top_k=top_k)))
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
        seen, items = set(), []
        for r in res:
            if r["url"] not in seen:
                seen.add(r["url"])
                items.append(_doc_item(r))
        return _nonempty(items[:2])

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
        return _nonempty([{"loai": "video", "tieu_de": r["title"], "url": r["url"], "kenh": r["channel"],
                        "phut": round(r["duration_sec"] / 60), "luot_xem": r["views"],
                        "thich": r["likes"], "nguoi_dang_ky": r["subscribers"], "mo_ta": r.get("description", "")} for r in res])

    return [search_documents, search_documents_reranked, search_web_documents, search_videos]