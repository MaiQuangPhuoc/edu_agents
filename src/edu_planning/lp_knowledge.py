import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import threading
from concurrent.futures import ThreadPoolExecutor
from src.clients.llm import build_prompt_messages
from src.state_plan import LessonKnowledge
from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_qa.paths import LP_CHAPTER_KNOWLEDGE_PROMPT_PATH
from src.edu_planning.lp_lesson_ctx import chapter_contexts, _lesson_plan_ctx, sgk_extra

MAX_WORKERS = 3
_ctx_lock = threading.Lock()       # embedding và rerank dùng chung 1 model, các chương chạy song song nên cần khóa

def _catalog(cur: dict) -> tuple[str, set]:
    text = "\n".join(f"chapter_id={cid} | {c['chapter_name']}: " + "; ".join(c["lessons"]) for cid, c in cur.items())
    return text, {(cid, l) for cid, c in cur.items() for l in c["lessons"]}

def _analyze_lesson(llm_client, subject, chapter_id, chapter, name, ctx, overview, catalog):
    """Trả (LessonKnowledge dict, lỗi hoặc None). Không có tài liệu thì không gọi LLM."""
    if ctx["source"] == "none":
        return LessonKnowledge(lesson=name).model_dump(), None
    messages = build_prompt_messages(LP_CHAPTER_KNOWLEDGE_PROMPT_PATH, {
        "subject": subject, "catalog": catalog, "chapter_id": chapter_id,
        "chapter_name": chapter["chapter_name"], "lesson": name, "source": ctx["source"],
        "overview": overview or "(không có)", "context": ctx["text"]})
    try:
        res = llm_client.invoke_structured(LessonKnowledge, messages, max_tokens=2500)
    except Exception as e:
        return LessonKnowledge(lesson=name).model_dump(), f"{type(e).__name__}: {str(e)[:150]}"
    if res is None:
        return LessonKnowledge(lesson=name).model_dump(), "không có kết quả"
    return res.model_dump(), None


def analyze_chapter(retriever, llm_client, subject: str, chapter_id: str) -> tuple[dict, list]:
    """Phân tích từng bài của chương (song song). Trả (dữ liệu chương, danh sách bài lỗi); không cache ở đây."""
    cur = get_subject_curriculum(subject)
    chapter = cur[chapter_id]
    names = list(chapter["lessons"])
    with _ctx_lock:
        ctxs = chapter_contexts(retriever, subject, chapter_id)
    for n in names:
        c = ctxs["lessons"][n]
        print(f"[knowledge] {subject} chương {chapter_id} | {n} | nguồn={c['source']} | {len(c['text'])} ký tự")
    catalog, valid = _catalog(cur)

    def run(n):
        return _analyze_lesson(llm_client, subject, chapter_id, chapter, n, ctxs["lessons"][n],
                               ctxs["overview"], catalog)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        outs = list(ex.map(run, names))

    lessons, failed = [], []
    for n, (ls, err) in zip(names, outs):
        ls["lesson"] = n
        ls["related"] = [r for r in ls["related"] if (r["chapter_id"], r["lesson"]) in valid and r["lesson"] != n]
        lessons.append(ls)
        if err:
            failed.append(n)
            print(f"[knowledge] lỗi bài {n}: {err}")
    return {"chapter_id": chapter_id, "lessons": lessons}, failed

def refine_lesson(retriever, llm_client, subject: str, chapter_id: str, name: str, query: str) -> dict | None:
    """Phân tích lại MỘT bài với giáo án (nếu có) cộng SGK tra thêm theo query. Trả None nếu không có thêm gì hoặc lỗi."""
    cur = get_subject_curriculum(subject)
    catalog, valid = _catalog(cur)
    with _ctx_lock:
        plan = _lesson_plan_ctx(retriever, subject, chapter_id, [name]).get(name, "")
        extra = sgk_extra(retriever, subject, chapter_id, query)
    if not extra:
        return None
    ctx = {"source": "lesson_plan" if plan else "sgk", "text": "\n".join(x for x in (plan, extra) if x)}
    ls, err = _analyze_lesson(llm_client, subject, chapter_id, cur[chapter_id], name, ctx, "", catalog)
    if err:
        print(f"[knowledge] refine lỗi bài {name}: {err}")
        return None
    ls["lesson"] = name
    ls["related"] = [r for r in ls["related"] if (r["chapter_id"], r["lesson"]) in valid and r["lesson"] != name]
    return ls