import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import json
from concurrent.futures import ThreadPoolExecutor
from src.configs import env_config
from src.state_plan import VerifyResult, ToolCallPlan
from src.clients.llm import build_prompt_messages
from src.edu_qa.paths import LP_VERIFY_PROMPT_PATH
from src.edu_planning.plan_search import run_calls, _pref
from src.edu_planning.lp_knowledge import refine_lesson
from src.edu_planning.lp_tools import _save_cache

MAX_WORKERS = 3
MAX_FOLLOW_UPS = 3
LOG_MAX_CHARS = 3500
_TOOL = {"web": "search_web_documents", "video": "search_videos"}


def _knowledge_view(k: dict | None) -> str:
    if not k:
        return "(chưa có phân tích kiến thức)"
    lines = []
    for ls in k["lessons"]:
        first = f" | ý chính đầu: {ls['key_points'][0]}" if ls["key_points"] else ""
        lines.append(f"- {ls['lesson']}: key_points={len(ls['key_points'])}, must_know={len(ls['must_know'])}, "
                     f"must_understand={len(ls['must_understand'])}, problem_types={len(ls['problem_types'])}{first}")
    return "\n".join(lines)


def _drop_urls(log: str, urls: list[str]) -> str:
    return "\n".join(l for l in log.split("\n") if not (l.startswith("- ") and any(u in l for u in urls)))


def _has_items(log: str) -> bool:
    return any(l.startswith("- [") and "(không có kết quả)" not in l and "lỗi:" not in l for l in log.split("\n"))


def verify_chapter(state, cid, k, r, retriever, llm_client, plan_client, tools):
    """Kiểm tra một chương (kiến thức k, kết quả tài nguyên r) và bổ sung theo yêu cầu. Trả (k, r) mới.
    Lỗi LLM được ném ra để verify_all quyết định thử lại."""
    w, sm = state["lp_window"], state["student_model"]
    subject = w["subject"]
    log = r["evidence"] if r else ""
    prefs = {x: _pref(sm).get(x) for x in ("dung_video", "dung_tai_lieu")}
    changed_k = False

    for rnd in range(1, max(1, env_config.lp_verify_rounds) + 1):
        messages = build_prompt_messages(LP_VERIFY_PROMPT_PATH, {
            "subject": subject, "chapter_id": cid, "chapter_name": w["chapter_names"].get(cid, ""),
            "prefs": json.dumps(prefs, ensure_ascii=False),
            "knowledge": _knowledge_view(k),
            "resources": log[:LOG_MAX_CHARS] if log else ("(không tra tài nguyên)" if not r else "(chưa có kết quả)")})
        res = llm_client.invoke_structured(VerifyResult, messages, max_tokens=2000)
        if res is None:
            break
        print(f"[verify] chương {cid} vòng {rnd}: đủ={res.sufficient} | thiếu={res.missing} | "
              f"bỏ url={len(res.irrelevant_urls)} | tra thêm={len(res.follow_up_queries)}")
        log = _drop_urls(log, [u for u in res.irrelevant_urls if u in log])

        names = {ls["lesson"] for ls in (k or {"lessons": []})["lessons"]}
        calls = [ToolCallPlan(tool=_TOOL[f.source], query=f.query, chapter_id=cid)
                 for f in res.follow_up_queries[:MAX_FOLLOW_UPS] if f.source in _TOOL]
        if calls and r is not None:
            log = (log + "\n" + run_calls(tools, calls, subject, [cid], sm)).strip()
        for f in res.follow_up_queries[:MAX_FOLLOW_UPS]:
            if f.source == "textbook" and f.lesson in names:
                new = refine_lesson(retriever, plan_client, subject, cid, f.lesson, f.query)
                if new:
                    k["lessons"] = [new if ls["lesson"] == f.lesson else ls for ls in k["lessons"]]
                    changed_k = True
        if res.sufficient or not res.follow_up_queries:
            break

    if changed_k and not k.get("failed_lessons"):
        _save_cache(subject, cid, k)             # kết quả đã bổ sung thì lưu lại cho lần sau
    if r is not None and _has_items(log):
        r = {"goal": r["goal"], "text": log, "evidence": log}
    return k, r


def verify_all(state, retriever, llm_client, plan_client, tools, results: dict, knowledge: dict):
    """Kiểm tra mọi chương. Song song nếu LP_VERIFY_PARALLEL; chương nào lỗi thì thử lại tuần tự một lần."""
    if not env_config.lp_verify:
        return results, knowledge
    cids = state["lp_window"]["chapter_ids"]

    def one(cid):
        return verify_chapter(state, cid, knowledge.get(cid), results.get(f"g_{cid}"), retriever, llm_client, plan_client, tools)

    done = {}
    if env_config.lp_verify_parallel:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            futs = {cid: ex.submit(one, cid) for cid in cids}
        for cid, f in futs.items():
            try:
                done[cid] = f.result()
            except Exception as e:
                print(f"[verify] chương {cid} lỗi khi chạy song song ({type(e).__name__}: {str(e)[:100]}), thử lại tuần tự")
    for cid in cids:
        if cid in done:
            continue
        try:
            done[cid] = one(cid)
        except Exception as e:
            print(f"[verify] chương {cid} lỗi, giữ kết quả chưa kiểm tra: {type(e).__name__}: {str(e)[:100]}")

    results, knowledge = dict(results), dict(knowledge)
    for cid, (k, r) in done.items():
        if k:
            knowledge[cid] = k
        if r is not None:
            results[f"g_{cid}"] = r
    return results, knowledge