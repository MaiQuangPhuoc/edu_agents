import os
from googleapiclient.discovery import build
from langchain_core.tools import tool

_youtube = None


import re as _re
import isodate  # pip install isodate


def _get_durations(video_ids: list[str]) -> dict:
    """Lấy duration (giây) cho list video_id."""
    yt = get_youtube_client()
    resp = yt.videos().list(
        part="contentDetails",
        id=",".join(video_ids),
    ).execute()
    result = {}
    for item in resp.get("items", []):
        dur_str = item["contentDetails"]["duration"]  # ISO 8601, vd PT15M33S
        seconds = int(isodate.parse_duration(dur_str).total_seconds())
        result[item["id"]] = seconds
    return result

def _llm_filter_titles(query: str, items: list[dict], llm_client, n: int = 5) -> list[dict]:
    """LLM chọn n title gần nhất với query. Trả về list item đã lọc."""
    if not items:
        return []

    title_list = "\n".join(f"{i}. {it['title']}" for i, it in enumerate(items))
    prompt = f"""Chủ đề cần tìm: {query}

Danh sách tiêu đề video:
{title_list}

Chọn {n} index LIÊN QUAN NHẤT đến chủ đề trên, sắp xếp theo độ liên quan giảm dần.
Chỉ trả về list số, ví dụ: 2,0,4
Không giải thích."""

    response = llm_client._llm.invoke([{"role": "user", "content": prompt}])
    raw = response.content.strip()

    try:
        indices = [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]
        return [items[i] for i in indices if i < len(items)]
    except Exception:
        return items[:n]
    
    
def get_youtube_client():
    global _youtube
    if _youtube is None:
        _youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
    return _youtube


LONG_VIDEO_THRESHOLD_SEC = 240  # >4 phút coi là "long"


@tool
def search_youtube_lecture(query: str, llm_client=None, max_results: int = 2) -> list[dict]:
    """Tìm video bài giảng Toán 10 trên YouTube theo chủ đề/bài học."""
    yt = get_youtube_client()
    try:
        resp = yt.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=10,          # lấy nhiều candidate trước khi lọc
            relevanceLanguage="vi",
        ).execute()
    except Exception as e:
        return [{"error": str(e)}]

    items = [
        {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
        }
        for item in resp.get("items", [])
    ]
    if not items:
        return []

    # Bước 1: LLM lọc theo title gần nhất
    if llm_client:
        items = _llm_filter_titles(query, items, llm_client, n=5)

    # Bước 2: hardcode lọc theo duration, chỉ giữ "long"
    durations = _get_durations([it["video_id"] for it in items])
    long_items = [it for it in items if durations.get(it["video_id"], 0) >= LONG_VIDEO_THRESHOLD_SEC]

    long_items = long_items[:max_results]

    return [
        {
            "title": it["title"],
            "channel": it["channel"],
            "url": f"https://youtube.com/watch?v={it['video_id']}",
            "duration_sec": durations.get(it["video_id"]),
        }
        for it in long_items
    ]