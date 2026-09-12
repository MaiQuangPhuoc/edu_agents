import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from langchain_core.tools import tool
from tavily import TavilyClient
from src.configs import env_config

TRUSTED_MATH_DOMAINS = [
    "toanmath.com", "vietjack.com", "loigiaihay.com", "hoc247.net", "moon.vn", "hocmai.vn",
]
TRUSTED_VAN_DOMAINS = [
    "vietjack.com", "loigiaihay.com", "hoc247.net", "tailieumoi.vn",
]
TRUSTED_SU_DOMAINS = [
    "vietjack.com", "loigiaihay.com", "hoc247.net", "sachgiaokhoa.com.vn", "lichsuvietnam.vn",
]

SUBJECT_DOMAIN_MAP = {
    "Toán 10": TRUSTED_MATH_DOMAINS,
    "Ngữ văn 10": TRUSTED_VAN_DOMAINS,
    "Lịch sử 10": TRUSTED_SU_DOMAINS,
}

_tavily_client = TavilyClient(api_key=env_config.api_key_tavily)


@tool
def web_search_edu(query: str, subject: str, max_results: int = 3) -> list[dict]:
    """Tìm kiếm thông tin học tập trên các trang web uy tín tại Việt Nam, lọc theo môn học.

    Chỉ dùng khi tài liệu nội bộ (vectorDB) không đủ để trả lời câu hỏi.

    Args:
        query: câu hỏi hoặc từ khóa cần tìm kiếm.
        subject: môn học, 1 trong "Toán 10" | "Ngữ văn 10" | "Lịch sử 10".
        max_results: số kết quả tối đa, mặc định 3.
    """
    domains = SUBJECT_DOMAIN_MAP.get(subject, [])
    try:
        response = _tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_domains=domains,
            include_answer=False,
        )
        results = response.get("results", [])
        return [
            {"title": r.get("title", ""), "url": r.get("url", ""), "content": r.get("content", "")}
            for r in results if r.get("content")
        ]
    except Exception:
        return []
    
print("web_search_math tool loaded. Trusted domains:")