import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from concurrent.futures import ThreadPoolExecutor
from src.state_plan import PlanState
from src.clients.llm import LLMClient
from src.edu_planning.lp_tools import _analyze
from src.edu_planning.planning_tools import make_planning_tools
from src.edu_planning.lp_resources import fetch_resources

MAX_WORKERS = 3


def _knowledge(task: dict, state: PlanState, retriever, plan_client: LLMClient) -> tuple[dict, dict | None]:
    data = _analyze(retriever, plan_client, state["lp_window"]["subject"], task["chapter_id"])
    if "error" in data:
        return {"goal": task["goal"], "text": f"THIẾU: {data['error']}", "evidence": ""}, None
    text = f"Đã phân tích {len(data['lessons'])} bài chương {task['chapter_id']}"
    if data.get("failed_lessons"):
        text += f"; THIẾU: bài lỗi {', '.join(data['failed_lessons'])}"
    return {"goal": task["goal"], "text": text, "evidence": ""}, data


def execute_node(state: PlanState, retriever, llm_client: LLMClient, plan_client: LLMClient | None = None) -> dict:
    print(">>> [LP] execute")
    plan_client = plan_client or llm_client
    tools = {t.name: t for t in make_planning_tools(retriever, llm_client)}

    def run(task):
        if task["kind"] == "knowledge":
            return task, *_knowledge(task, state, retriever, plan_client)
        return task, fetch_resources(task, state, llm_client, tools), None

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        outs = list(ex.map(run, state["lp_tasks"]))       # các việc độc lập nhau nên chạy song song
    results = {t["id"]: r for t, r, _ in outs}
    knowledge = {t["chapter_id"]: k for t, _, k in outs if k}
    return {"lp_results": results, "lp_knowledge": knowledge, "current_step": "learning_path"}