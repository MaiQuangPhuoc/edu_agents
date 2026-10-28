import os

ON = os.getenv("LP_DEBUG", "1") != "0"          # LP_DEBUG=0 để tắt


def _p(*a):
    print("   ", *a, flush=True)


def _outline(u, s):
    for ph in u.get("lp_outline", []):
        _p(f"[giai đoạn {ph['phase']}]")
        for w in ph["weeks"]:
            les = "; ".join(f"{l['chapter_id']}:{l['lesson']}" for l in w["lessons"])
            _p(f"T{w['week_no']}{' (KT)' if w['has_assessment'] else ''} {w['goal'][:70]} | {les}")


def _plan(u, s):
    w = u.get("lp_window", {})
    _p(f"môn={w.get('subject')} giai đoạn={w.get('phase')} số tuần={w.get('num_weeks')}")
    for t in u.get("lp_tasks", []):
        _p(f"task {t['id']} ({t['kind']}): {t['goal'][:80]}")


def _execute(u, s):
    for cid, d in u.get("lp_knowledge", {}).items():
        for l in d.get("lessons", []):
            _p(f"[kiến thức {cid}] {l.get('lesson')}: ý chính={len(l.get('key_points', []))} "
               f"must_know={len(l.get('must_know', []))} dạng bài={len(l.get('problem_types', []))}")
        if d.get("failed_lessons"):
            _p(f"[kiến thức {cid}] LỖI: {d['failed_lessons']}")
    for tid, r in u.get("lp_results", {}).items():
        if tid.startswith("g_"):
            items = r.get("items", [])
            _p(f"[tài nguyên {tid}] {len(items)} mục" + ("" if items else f" - {r['text'][:100]}"))
            for it in items:
                _p(f"   - {it.get('kind')}|{it.get('purpose')} {it.get('title', '')[:60]} | {it.get('url')} | bài: {it.get('lesson', '')}")


def _draft(u, s):
    d = u.get("lp_draft", {})
    if "error" in d:
        return _p("LỖI:", d["error"])
    for w in d.get("weeks", []):
        _p(f"Tuần {w['week_no']}: {w.get('goal', '')[:60]}")
        for x in w["sessions"]:
            kinds = ",".join(a["type"] for a in x["activities"])
            _p(f"   {x['type']} {x['lesson']} | hoạt động: {kinds} | tài nguyên: " + "; ".join(r["title"][:40] for r in x["resources"]))
    for a in d.get("assumptions", []):
        _p("ghi chú:", a)


def _critic(u, s):
    _p(f"lần sửa={u.get('lp_revision_count')} đã review={u.get('lp_reviewed')}")
    iss = u.get("lp_issues", {})
    for k, v in iss.items():
        for x in v:
            _p(f"tuần {k}: {x}")
    if not iss:
        _p("không có lỗi")


def _present(u, s):
    _p(u.get("roadmap_status"), u.get("lp_file", ""))


_SHOW = {"outline": _outline, "plan": _plan, "execute": _execute, "assemble": _draft, "critic": _critic, "present": _present}


def traced(name, fn):
    def run(state):
        out = fn(state)
        if ON:
            print(f"=== [LP:{name}] kết quả ===", flush=True)
            try:
                _SHOW[name](out, state)
            except Exception as e:                   # lỗi khi in không được làm hỏng luồng
                _p("(không in được:", repr(e), ")")
        return out
    return run