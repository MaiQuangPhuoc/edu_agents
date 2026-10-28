import sys, os, re, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from concurrent.futures import ThreadPoolExecutor
from src.state_plan import ResourceQueryPlan, ResourceVerdict
from src.clients.llm import build_prompt_messages
from src.edu_qa.paths import LP_RESOURCES_PROMPT_PATH, LP_VERIFY_PROMPT_PATH
from src.edu_planning.plan_search import _pref
from src.edu_planning.lp_plan import student_text
from src.edu_planning.lp_tools import _norm
from src.configs import env_config

MAX_QUERIES = 6                 # số query tối đa mỗi chương
MAX_ITEMS = 10                  # số tài nguyên tối đa giữ lại mỗi chương

PER_GROUP = 2                   # số mục giữ lại cho mỗi cặp (loại, mục đích) sau cùng
PER_GROUP_FETCH = 3             # số mục đưa vào bước kiểm bằng LLM cho mỗi cặp
# độ dài video hợp lý (phút) theo mục đích; ngoài khoảng này điểm bị giảm một nửa
_FIT = {"theory": (8, 60), "practice": (8, 90), "review": (15, 120), "exam": (0, 999)}


_TOOL = {"video": "search_videos", "web": "search_web_documents"}
_STOP = {"bai", "chuong", "cac", "cua", "va", "toan", "lop", "hoc", "van", "su", "mot", "nhung"}
_GRADE = re.compile(r"(?:l[oớ]p|to[aá]n|v[aă]n|s[uử])\s*(\d{1,2})", re.I)     # "lớp 11", "Toán 11", "Văn 12"...


def _allowed(sm: dict, kind: str) -> bool:
    p = _pref(sm)
    return bool(p.get("dung_video")) if kind == "video" else p.get("dung_tai_lieu") is not False


def plan_queries(task: dict, state, llm_client) -> list:
    """LLM nghĩ nhiều query ứng viên rồi tự lọc vài query tốt nhất. Chỉ giữ query hợp sở thích học."""
    w, cid, sm = state["lp_window"], task["chapter_id"], state["student_model"]
    messages = build_prompt_messages(LP_RESOURCES_PROMPT_PATH, {
        "student_model": student_text(sm), "subject": w["subject"], "chapter_id": cid,
        "chapter_name": w["chapter_names"].get(cid, ""), "max_queries": MAX_QUERIES,
        "lessons": "\n".join(f"- {l}" for l in w["chapter_lessons"][cid])})
    plan = llm_client.invoke_structured(ResourceQueryPlan, messages, max_tokens=1500)
    if plan is None:
        return []
    picked = plan.chosen or plan.candidates
    seen, out = set(), []
    for q in picked:
        key = (q.tool, q.query.strip().lower())
        if q.query.strip() and key not in seen and _allowed(sm, q.tool):
            seen.add(key)
            out.append(q)
    return out[:MAX_QUERIES]


def _item(q, r: dict) -> dict | None:
    if not isinstance(r, dict) or "loi" in r or "thong_bao" in r or not str(r.get("url", "")).startswith("http"):
        return None
    it = {"kind": q.tool, "purpose": q.purpose, "title": r.get("tieu_de", ""), "url": r["url"],
          "desc": (r.get("mo_ta") or "")[:300].replace("\n", " ")}
    if q.tool == "video":
        it.update(channel=r.get("kenh", "?"), minutes=r.get("phut"), views=r.get("luot_xem"),
                  likes=r.get("thich"), subs=r.get("nguoi_dang_ky"))
        it["meta"] = f"kênh {it['channel']} | {it['minutes']} phút"
    else:
        it["meta"] = " | ".join(x for x in (f"{r['so_trang']} trang" if r.get("so_trang") else "", r.get("ngay") or "") if x)
    return it


def search_all(queries: list, subject: str, tools: dict, tag: str = "") -> list[dict]:
    """Tra song song; mỗi lần tra một công cụ. Lỗi một lần tra không làm hỏng các lần khác."""
    def one(q):
        text = q.query if subject.lower() in q.query.lower() else f"{subject} {q.query}"
        try:
            res = tools[_TOOL[q.tool]].invoke({"query": text, "subject": subject})
        except Exception as e:
            print(f"[resources {tag}] lỗi {q.tool} '{q.query}': {type(e).__name__} {str(e)[:100]}")
            return []
        items = [i for i in (_item(q, r) for r in res or []) if i]
        print(f"[resources {tag}] tra {q.tool}/{q.purpose}: \"{q.query}\" -> {len(items)} kết quả")
        for i in items[:5]:
            print(f"      · {i['title'][:70]} | {i['meta']}")
        return items
    with ThreadPoolExecutor(max_workers=MAX_QUERIES) as ex:
        return [i for part in ex.map(one, queries) for i in part]


def _tokens(text: str) -> set:
    return {t for t in re.findall(r"[a-z0-9]+", _norm(text)) if len(t) >= 3 and t not in _STOP}


def code_check(items: list[dict], chapter_name: str, lessons: list[str]) -> list[dict]:
    """Kiểm bằng code, rẻ và chắc chắn: bỏ trùng url, sai lớp, tiêu đề không chứa từ khóa nào của chương/bài."""
    want = _tokens(chapter_name) | _tokens(" ".join(lessons))
    seen, out = set(), []
    for it in items:
        if it["url"] in seen:
            continue
        grades = {int(g) for g in _GRADE.findall(it["title"])}
        if grades and 10 not in grades:
            continue
        if want and not (_tokens(it["title"] + " " + it["url"]) & want):
            continue
        seen.add(it["url"])
        out.append(it)
    return out

def video_score(it: dict) -> float:
    """Điểm chất lượng 0..1 từ lượt xem, tỉ lệ thích/xem, số đăng ký kênh, độ dài hợp mục đích. Thiếu số liệu thì lấy 0.5."""
    views, likes, subs, mins = it.get("views"), it.get("likes"), it.get("subs"), it.get("minutes")
    v = min(math.log10(views + 1) / 6, 1) if views is not None else 0.5          # 1 triệu lượt xem = 1
    like = min(likes / views / 0.04, 1) if views and likes is not None else 0.5     # 4% thích/xem = 1
    sub = min(math.log10(subs + 1) / 6, 1) if subs is not None else 0.5
    lo, hi = _FIT.get(it["purpose"], (0, 999))
    fit = 1 if mins is None or lo <= mins <= hi else 0.5
    return (0.4 * v + 0.3 * like + 0.3 * sub) * fit


def top_per_group(items: list[dict], n: int) -> list[dict]:
    """Mỗi cặp (loại, mục đích) giữ n mục: video theo điểm chất lượng, tài liệu theo thứ tự tra."""
    groups = {}
    for it in items:
        groups.setdefault((it["kind"], it["purpose"]), []).append(it)
    out = []
    for (kind, _), g in groups.items():
        out += sorted(g, key=video_score, reverse=True)[:n] if kind == "video" else g[:n]
    return out


def _line(i: int, it: dict) -> str:
    stats = ""
    if it["kind"] == "video":
        stats = f" | {it['channel']} ({it['subs'] if it['subs'] is not None else '?'} đăng ký) | {it['minutes']} phút | " \
                f"{it['views'] if it['views'] is not None else '?'} xem, {it['likes'] if it['likes'] is not None else '?'} thích"
    return f"[{i}] {it['kind']}/{it['purpose']} | {it['title']}{stats} | mô tả: {it['desc'] or '(không có)'}"


def llm_verify(items: list[dict], chapter_name: str, lessons: list[str], llm_client) -> list[dict]:
    """LLM đánh giá từng mục chỉ từ siêu dữ liệu (tiêu đề, kênh, số liệu, mô tả): giữ/bỏ và gắn bài. Lỗi thì giữ nguyên."""
    messages = build_prompt_messages(LP_VERIFY_PROMPT_PATH, {
        "chapter_name": chapter_name, "lessons": "\n".join(f"- {l}" for l in lessons),
        "items": "\n".join(_line(i, it) for i, it in enumerate(items))})
    try:
        res = llm_client.invoke_structured(ResourceVerdict, messages, max_tokens=2000)
    except Exception as e:
        print(f"[resources] LLM kiểm lỗi, giữ nguyên: {type(e).__name__} {str(e)[:100]}")
        return items
    if res is None:
        return items
    verdict = {v.id: v for v in res.items}
    out = []
    for i, it in enumerate(items):
        v = verdict.get(i)
        if v and not v.keep:
            print(f"[resources] LLM BỎ: {it['title'][:60]} | {v.reason[:80]}")
            continue
        out.append({**it, "lesson": v.lesson if v and v.lesson in lessons else ""})
    return out
_HEAD = re.compile(r"^\[Tra cứu\] \S+ \(chương ([^)]+)\):")
_ROW = re.compile(r"^- \[(video|tài liệu)\] (.+?) \|(?: (.+?) \|)? (https?://\S+)\s*$")


def seed_items(transcript: str, chapter_id: str) -> list[dict]:
    """Lấy lại kết quả tra tài nguyên mà bước lập sườn đã tìm (nhật ký plan_transcript) cho một chương."""
    cur, out = None, []
    for line in transcript.split("\n"):
        m = _HEAD.match(line)
        if m:
            cur = m.group(1).strip()
            continue
        r = _ROW.match(line)
        if r and cur == chapter_id:
            kind = "video" if r.group(1) == "video" else "web"
            extra = r.group(3) or ""
            ch, mins = re.search(r"kênh (.+?) \(", extra), re.search(r"(\d+) phút", extra)
            it = {"kind": kind, "purpose": "chung", "title": r.group(2), "url": r.group(4), "desc": "", "meta": "",
                  "source": "sườn"}
            if kind == "video":
                it.update(channel=ch.group(1) if ch else "?", minutes=int(mins.group(1)) if mins else None,
                          views=None, likes=None, subs=None)
                it["meta"] = f"kênh {it['channel']} | {it['minutes']} phút"
            out.append(it)
    return out

def items_text(items: list[dict]) -> str:
    return "\n".join(f"- [{i['kind']}|{i['purpose']}] {i['title']} | " + (f"{i['meta']} | " if i["meta"] else "") + i["url"]
                     + (f" | bài: {i['lesson']}" if i.get("lesson") else "") for i in items)


def fetch_resources(task: dict, state, llm_client, tools: dict) -> dict:
    """Việc g_<chương>: LLM lập query -> tra song song -> kiểm bằng code -> (nếu bật) LLM kiểm ngữ nghĩa."""
    w, cid = state["lp_window"], task["chapter_id"]
    name, lessons = w["chapter_names"].get(cid, ""), w["chapter_lessons"][cid]
    try:
        queries = plan_queries(task, state, llm_client)
    except Exception as e:
        return {"goal": task["goal"], "text": f"THIẾU: lỗi lập query ({str(e)[:100]})", "evidence": ""}
    if not queries:
        return {"goal": task["goal"], "text": "THIẾU: không có query hợp lệ", "evidence": ""}
    tag = f"chương {cid}"
    print(f"[resources {tag}] ===== {name} | {len(lessons)} bài: {'; '.join(lessons)}")
    print(f"[resources {tag}] LLM chọn {len(queries)} query: " + " || ".join(f"{q.tool}/{q.purpose}: {q.query}" for q in queries))
    seeds = seed_items(state.get("plan_transcript", ""), cid)
    found = search_all(queries, w["subject"], tools, tag) + seeds                   # thêm kết quả của sườn
    checked = code_check(found, name, lessons)
    print(f"[resources {tag}] tìm {len(found) - len(seeds)} + {len(seeds)} từ sườn -> sau kiểm code còn {len(checked)}")
    items = top_per_group(checked, PER_GROUP_FETCH)
    use_llm = bool(items) and state.get("lp_verify", env_config.lp_verify)
    if use_llm:
        items = llm_verify(items, name, lessons, llm_client)
    print(f"[resources {tag}] LLM kiểm: {'bật' if use_llm else 'tắt'} -> còn {len(items)}")
    items = top_per_group(items, PER_GROUP)[:MAX_ITEMS]
    for i in items:
        print(f"[resources {tag}] GIỮ [{i['kind']}|{i['purpose']}] bài \"{i.get('lesson') or 'cả chương'}\": {i['title'][:70]} | {i['url']}")
    if items and state.get("lp_verify", env_config.lp_verify):
        items = llm_verify(items, name, lessons, llm_client)
    items = top_per_group(items, PER_GROUP)[:MAX_ITEMS]
    if not items:
        return {"goal": task["goal"], "text": "THIẾU: không tìm được tài liệu hoặc video phù hợp", "evidence": ""}
    text = items_text(items)
    return {"goal": task["goal"], "text": text, "evidence": text, "items": items}