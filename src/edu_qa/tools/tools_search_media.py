import os, threading
import re as _re
import isodate   
from googleapiclient.discovery import build
from langchain_core.tools import tool

_youtube = None
_yt_lock = threading.Lock()   # googleapiclient không thread-safe

import threading
_yt_lock = threading.Lock()   # googleapiclient không thread-safe

def _get_details(video_ids: list[str]) -> dict:
    yt = get_youtube_client()
    resp = yt.videos().list(part="contentDetails,statistics", id=",".join(video_ids)).execute()
    out = {}
    for it in resp.get("items", []):
        st = it.get("statistics", {})
        out[it["id"]] = {
            "duration": int(isodate.parse_duration(it["contentDetails"]["duration"]).total_seconds()),
            "views": int(st["viewCount"]) if "viewCount" in st else None,
            "likes": int(st["likeCount"]) if "likeCount" in st else None,
        }
    return out

def _get_subs(channel_ids: list[str]) -> dict:
    yt = get_youtube_client()
    resp = yt.channels().list(part="statistics", id=",".join(set(channel_ids))).execute()
    out = {}
    for it in resp.get("items", []):
        st = it.get("statistics", {})
        out[it["id"]] = None if st.get("hiddenSubscriberCount") else int(st.get("subscriberCount", 0))
    return out

def get_youtube_client():
    global _youtube
    if _youtube is None:
        _youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
    return _youtube


LONG_VIDEO_THRESHOLD_SEC = 240  # >4 phút coi là "long"


@tool
def search_youtube_lecture(query: str, llm_client=None, max_results: int = 2) -> list[dict]:
    """Tìm video bài giảng trên YouTube theo chủ đề/bài học (giữ thứ tự YouTube, chỉ lấy video dài)."""
    with _yt_lock:
        try:
            yt = get_youtube_client()
            resp = yt.search().list(q=query, part="snippet", type="video",
                                    maxResults=10, relevanceLanguage="vi").execute()
            items = [{"video_id": i["id"]["videoId"], "title": i["snippet"]["title"],
                      "channel": i["snippet"]["channelTitle"], "channel_id": i["snippet"]["channelId"]}
                     for i in resp.get("items", [])]
            if not items:
                return []
            det = _get_details([it["video_id"] for it in items])
            items = [it for it in items
                     if det.get(it["video_id"], {}).get("duration", 0) >= LONG_VIDEO_THRESHOLD_SEC][:max_results]
            subs = _get_subs([it["channel_id"] for it in items]) if items else {}
        except Exception as e:
            return [{"error": str(e)}]
    return [{"title": it["title"], "channel": it["channel"],
             "url": f"https://youtube.com/watch?v={it['video_id']}",
             "duration_sec": det[it["video_id"]]["duration"],
             "views": det[it["video_id"]]["views"], "likes": det[it["video_id"]]["likes"],
             "subscribers": subs.get(it["channel_id"])} for it in items]