import json

MAX_CALLS = 5


def _empty(res) -> bool:
    return not res or (len(res) == 1 and "thong_bao" in res[0])


def _call(tool, args: dict):
    try:
        return tool.invoke(args)
    except Exception as e:
        return [{"loi": f"{type(e).__name__}: {str(e)[:150]}"}]


def run_calls(tools: dict, calls: list, subject: str, allowed: list, sm: dict) -> str:
    """Chạy tuần tự các lần tra do LLM lập (tối đa MAX_CALLS). Trả về nhật ký tra cứu dạng text."""
    pref = sm.get("so_thich_hoc") or {}
    pref = pref[0] if isinstance(pref, list) and pref else pref if isinstance(pref, dict) else {}
    lines = []
    for c in calls[:MAX_CALLS]:
        if c.tool == "search_videos" and not pref.get("dung_video"):
            continue
        if c.tool == "search_web_documents" and pref.get("dung_tai_lieu") is False:
            continue
        if c.chapter_id and c.chapter_id not in allowed:
            print(f"[planning] bỏ lần tra ngoài phạm vi: {c.tool} chương {c.chapter_id}")
            continue
        args = {"query": c.query, "subject": subject}
        if c.chapter_id and c.tool in ("search_documents", "search_documents_reranked"):
            args["chapter_id"] = c.chapter_id
        res = _call(tools[c.tool], args)
        if _empty(res) and "chapter_id" in args:        # rỗng: thử lại một lần, bỏ chapter_id
            args.pop("chapter_id")
            res = _call(tools[c.tool], args)
        n = 0 if _empty(res) else len(res)
        print(f"[planning] tra: {c.tool} {args} -> {n} kết quả")
        lines.append(f"[Tra cứu] {c.tool}({json.dumps(args, ensure_ascii=False)})\n"
                     f"[Kết quả] {json.dumps(res, ensure_ascii=False)[:3000]}")
    return "\n".join(lines) or "(không tra cứu)"