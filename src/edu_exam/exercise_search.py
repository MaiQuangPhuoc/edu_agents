"""Tìm bài tập/đề ôn trên các trang uy tín. Chỉ trả danh sách tên đề, nguồn, link; không đổi nội dung."""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from urllib.parse import urlparse

MAX_TESTS = 6
_KEYS = ("bài tập", "đề", "trắc nghiệm", "ôn tập", "ôn thi", "luyện")


def _domain(url: str) -> str:
    return urlparse(url).netloc.removeprefix("www.")


def find_tests(subject: str, chapter_name: str, lesson: str, topics: list[str] | None = None) -> list[dict]:
    """[{title, source, url}] không trùng url. Lỗi tìm kiếm thì bỏ qua truy vấn đó."""
    from src.edu_qa.tools.web_search_tool import web_search_edu          # import muộn: chỉ nạp Tavily khi dùng
    queries = [f"bài tập trắc nghiệm {lesson} {chapter_name} lớp 10 có đáp án"]
    queries += [f"bài tập {t} {lesson} lớp 10" for t in (topics or [])[:2]]
    out, seen = [], set()
    for q in queries:
        try:
            res = web_search_edu.invoke({"query": q, "subject": subject, "max_results": 4})
        except Exception as e:
            print(f"[find_tests] lỗi '{q}': {type(e).__name__} {str(e)[:80]}")
            continue
        for r in res or []:
            url, title = r.get("url", ""), (r.get("title") or "").strip()
            text = f"{title} {url} {r.get('content', '')[:200]}".lower()
            if url and url not in seen and title and any(k in text for k in _KEYS):
                seen.add(url)
                out.append({"title": title, "source": _domain(url), "url": url})
    print(f"[find_tests] {lesson}: {len(out)} bài")
    return out[:MAX_TESTS]


def tests_text(tests: list[dict]) -> str:
    if not tests:
        return ""
    return "Các bài tập theo chủ đề bạn có thể ôn tập:\n" + "\n".join(f"- {t['title']} : {t['source']} : {t['url']}" for t in tests)
