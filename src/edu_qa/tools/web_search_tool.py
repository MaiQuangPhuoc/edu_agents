import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from langchain_core.tools import tool
from tavily import TavilyClient
from src.configs import env_config

TRUSTED_MATH_DOMAINS = [
    "toanmath.com",
    "vietjack.com",
    "loigiaihay.com",
    "hoc247.net",
    "moon.vn",
    "hocmai.vn",
]

_tavily_client = TavilyClient(api_key=env_config.api_key_tavily)


@tool
def web_search_math(query: str, max_results: int = 5) -> list[dict]:
    """Tìm kiếm thông tin Toán học trên các trang web uy tín tại Việt Nam.

    Chỉ dùng khi tài liệu nội bộ (vectorDB) không đủ để trả lời câu hỏi.
    Chỉ trả về nội dung dạng văn bản (text), KHÔNG lấy link video/YouTube.

    Args:
        query: câu hỏi hoặc từ khóa cần tìm kiếm.
        max_results: số kết quả tối đa cần lấy, mặc định 5.

    Returns:
        Danh sách dict, mỗi dict gồm {"title": ..., "url": ..., "content": ...}.
        Trả về danh sách rỗng nếu không tìm được kết quả phù hợp.
    """
    try:
        response = _tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_domains=TRUSTED_MATH_DOMAINS,
            include_answer=False,
        )
        results = response.get("results", [])

        return [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", ""),
            }
            for r in results
            if r.get("content")
        ]
    except Exception as e:
        return []
    
print("web_search_math tool loaded. Trusted domains:")