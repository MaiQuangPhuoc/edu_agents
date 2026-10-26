import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from concurrent.futures import ThreadPoolExecutor
from src.state_plan import PlanState, ToolPlan
from src.clients.llm import LLMClient, build_prompt_messages
from src.edu_qa.paths import LP_RESOURCES_PROMPT_PATH
from src.edu_planning.lp_tools import _analyze
from src.edu_planning.planning_tools import make_planning_tools
from src.edu_planning.plan_search import run_calls
from src.edu_planning.lp_plan import student_text

MAX_WORKERS = 3


def _knowledge(task: dict, state: PlanState, retriever, plan_client: LLMClient) -> tuple[dict, dict | None]:
    data = _analyze(retriever, plan_client, state["lp_window"]["subject"], task["chapter_id"])
    if "error" in data:
        return {"goal": task["goal"], "text": f"THIẾU: {data['error']}", "evidence": ""}, None
    text = f"Đã phân tích {len(data['lessons'])} bài chương {task['chapter_id']}"
    if data.get("failed_lessons"):
        text += f"; THIẾU: bài lỗi {', '.join(data['failed_lessons'])}"
    return {"goal": task["goal"], "text": text, "evidence": ""}, data


def _resources(task: dict, state: PlanState, llm_client: LLMClient, tools: dict) -> dict:
    w, cid = state["lp_window"], task["chapter_id"]
    messages = build_prompt_messages(LP_RESOURCES_PROMPT_PATH, {
        "student_model": student_text(state["student_model"]), "subject": w["subject"],
        "chapter_id": cid, "chapter_name": w["chapter_names"].get(cid, ""),
        "lessons": "\n".join(f"- {l}" for l in w["chapter_lessons"][cid])})
    try:
        plan = llm_client.invoke_structured(ToolPlan, messages, max_tokens=1500)
    except Exception as e:
        return {"goal": task["goal"], "text": f"THIẾU: lỗi lập kế hoạch tra cứu ({str(e)[:100]})", "evidence": ""}
    log = run_calls(tools, plan.calls if plan else [], w["subject"], [cid], state["student_model"])
    if not log or log.count("(không có kết quả)") == log.count("[Tra cứu]"):
        return {"goal": task["goal"], "text": "THIẾU: không tìm được tài liệu hoặc video", "evidence": log}
    return {"goal": task["goal"], "text": log, "evidence": log}


def execute_node(state: PlanState, retriever, llm_client: LLMClient, plan_client: LLMClient | None = None) -> dict:
    print(">>> [LP] execute")
    plan_client = plan_client or llm_client
    tools = {t.name: t for t in make_planning_tools(retriever, llm_client)}

    def run(task):
        if task["kind"] == "knowledge":
            return task, *_knowledge(task, state, retriever, plan_client)
        return task, _resources(task, state, llm_client, tools), None

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        outs = list(ex.map(run, state["lp_tasks"]))       # các việc độc lập nhau nên chạy song song
    results = {t["id"]: r for t, r, _ in outs}
    knowledge = {t["chapter_id"]: k for t, _, k in outs if k}
    return {"lp_results": results, "lp_knowledge": knowledge, "current_step": "learning_path"}