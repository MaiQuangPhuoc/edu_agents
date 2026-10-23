import json

MAX_CALLS = 4


def _pref(sm: dict) -> dict:
    p = sm.get("so_thich_hoc") or {}
    return p[0] if isinstance(p, list) and p else p if isinstance(p, dict) else {}


def wants_resources(sm: dict) -> bool:
    """Chỉ lập kế hoạch tra web/video khi học sinh có dùng ít nhất một loại."""
    p = _pref(sm)
    return bool(p.get("dung_video")) or p.get("dung_tai_lieu") is not False


def _empty(res) -> bool:
    return not res or (len(res) == 1 and "thong_bao" in res[0])


def _call(tool, args: dict):
    try:
        return tool.invoke(args)
    except Exception as e:
        return [{"loi": f"{type(e).__name__}: {str(e)[:150]}"}]


def run_calls(tools: dict, calls: list, subject: str, allowed: list, sm: dict) -> str:
    """Chạy tuần tự các lần tra web/video do LLM lập. Trả về nhật ký tra cứu dạng text."""
    p = _pref(sm)
    lines = []
    for c in calls[:MAX_CALLS]:
        if c.tool == "search_videos" and not p.get("dung_video"):
            continue
        if c.tool == "search_web_documents" and p.get("dung_tai_lieu") is False:
            continue
        if c.chapter_id and c.chapter_id not in allowed:
            print(f"[planning] bỏ lần tra ngoài phạm vi: {c.tool} chương {c.chapter_id}")
            continue
        args = {"query": c.query, "subject": subject}
        res = _call(tools[c.tool], args)
        print(f"[planning] tra: {c.tool} {args} -> {0 if _empty(res) else len(res)} kết quả")
        lines.append(f"[Tra cứu] {c.tool}({json.dumps(args, ensure_ascii=False)})\n"
                     f"[Kết quả] {json.dumps(res, ensure_ascii=False)[:3000]}")
    return "\n".join(lines)