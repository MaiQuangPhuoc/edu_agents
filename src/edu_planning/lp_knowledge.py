import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import math, threading
from concurrent.futures import ThreadPoolExecutor
from src.clients.llm import build_prompt_messages
from src.state_plan import ChapterKnowledge, LessonKnowledge
from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_qa.paths import LP_CHAPTER_KNOWLEDGE_PROMPT_PATH
from src.edu_planning.lp_lesson_ctx import chapter_contexts, _lesson_plan_ctx, sgk_extra

MAX_WORKERS = 3
GROUP_SIZE = 3                  # tối đa số bài phân tích trong một lần gọi
_ctx_lock = threading.Lock()    # embedding và rerank dùng chung 1 model, các chương chạy song song nên cần khóa


def _catalog(cur: dict) -> tuple[str, set]:
    text = "\n".join(f"chapter_id={cid} | {c['chapter_name']}: " + "; ".join(c["lessons"]) for cid, c in cur.items())
    return text, {(cid, l) for cid, c in cur.items() for l in c["lessons"]}


def _groups(names: list, size: int = GROUP_SIZE) -> list[list]:
    """Chia đều, giữ thứ tự: 4 bài -> [2, 2]; 5 bài -> [2, 3]; 3 bài -> [3]."""
    n = math.ceil(len(names) / size) or 1
    cut = [round(i * len(names) / n) for i in range(n + 1)]
    return [names[cut[i]:cut[i + 1]] for i in range(n) if cut[i] < cut[i + 1]]


def _block(name: str, ctx: dict) -> str:
    return (f"### {name}\n[Giáo án]\n{ctx['plan'] or '(không có)'}\n[SGK]\n{ctx['sgk'] or '(không có)'}")


def _analyze_group(llm_client, subject, chapter_id, chapter, names, ctxs, catalog, valid) -> tuple[dict, str | None]:
    """Phân tích một nhóm bài trong một lần gọi. Trả ({tên bài: LessonKnowledge dict}, lỗi hoặc None).
    Bài không có tài liệu nào thì không đưa vào lời gọi (kết quả rỗng)."""
    have = [n for n in names if ctxs[n]["plan"] or ctxs[n]["sgk"]]
    out = {n: LessonKnowledge(lesson=n).model_dump() for n in names}
    if not have:
        return out, None
    messages = build_prompt_messages(LP_CHAPTER_KNOWLEDGE_PROMPT_PATH, {
        "subject": subject, "catalog": catalog, "chapter_id": chapter_id, "chapter_name": chapter["chapter_name"],
        "lessons": "\n".join(f"- {n}" for n in have), "context": "\n\n".join(_block(n, ctxs[n]) for n in have)})
    try:
        res = llm_client.invoke_structured(ChapterKnowledge, messages, max_tokens=4500)
    except Exception as e:
        return out, f"{type(e).__name__}: {str(e)[:150]}"
    if res is None:
        return out, "không có kết quả"
    for ls in res.model_dump()["lessons"]:
        if ls["lesson"] in have:
            ls["related"] = [r for r in ls["related"] if (r["chapter_id"], r["lesson"]) in valid and r["lesson"] != ls["lesson"]]
            out[ls["lesson"]] = ls
    miss = [n for n in have if not out[n]["key_points"]]
    return out, (f"thiếu kết quả bài: {', '.join(miss)}" if miss else None)


def analyze_chapter(retriever, llm_client, subject: str, chapter_id: str) -> tuple[dict, list]:
    """Phân tích chương theo nhóm 2-3 bài (nhóm chạy song song). Trả (dữ liệu chương, danh sách bài lỗi); không cache ở đây."""
    cur = get_subject_curriculum(subject)
    chapter = cur[chapter_id]
    names = list(chapter["lessons"])
    with _ctx_lock:
        ctxs = chapter_contexts(retriever, subject, chapter_id)["lessons"]
    for n in names:
        print(f"[knowledge] {subject} chương {chapter_id} | {n} | giáo án={len(ctxs[n]['plan'])} ký tự | SGK={len(ctxs[n]['sgk'])} ký tự")
    catalog, valid = _catalog(cur)
    groups = _groups(names)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        outs = list(ex.map(lambda g: _analyze_group(llm_client, subject, chapter_id, chapter, g, ctxs, catalog, valid), groups))

    by_name, failed = {}, []
    for g, (part, err) in zip(groups, outs):
        by_name.update(part)
        if err:
            print(f"[knowledge] lỗi nhóm {g}: {err}")
            failed += [n for n in g if not part[n]["key_points"] and (ctxs[n]["plan"] or ctxs[n]["sgk"])]
    return {"chapter_id": chapter_id, "lessons": [by_name[n] for n in names]}, failed


