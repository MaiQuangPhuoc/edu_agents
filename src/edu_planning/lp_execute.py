import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from concurrent.futures import ThreadPoolExecutor
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.errors import GraphRecursionError
from src.state_plan import PlanState
from src.clients.llm import LLMClient
from src.edu_qa.paths import LP_EXECUTOR_PROMPT_PATH
from src.edu_planning.lp_tools import make_lp_tools, _load_cache
from src.edu_planning.planning_tools import make_planning_tools
from src.edu_planning.lp_plan import window_text, student_text

MAX_WORKERS = 3
ALLOWED = {"F1": ["analyze_chapter_knowledge"]}


def _run_task(task: dict, tools: dict, state: PlanState, llm_client: LLMClient, results: dict):
    w = state["lp_window"]
    names = ALLOWED.get(task["id"], list(tools))          # bước LLM sinh được dùng mọi tool
    max_calls = len(w["chapter_ids"]) + 1 if task["id"] == "F1" else 3
    prev = "\n\n".join(f"[{d}] {results[d]['text']}" for d in task["depends_on"] if d in results) or "(không có)"
    prompt = (LP_EXECUTOR_PROMPT_PATH.read_text(encoding="utf-8")
              .replace("{goal}", task["goal"])
              .replace("{student_model}", student_text(state["student_model"]))
              .replace("{window}", window_text(w))
              .replace("{previous_results}", prev)
              .replace("{max_calls}", str(max_calls)))
    agent = create_agent(llm_client._llm, [tools[n] for n in names])

    text, evidence = "", ""
    for _ in range(2 if task["origin"] == "fixed" else 1):     # bước cố định thử lại 1 lần
        try:
            res = agent.invoke({"messages": [HumanMessage(content=prompt)]},
                               config={"recursion_limit": 2 * max_calls + 1})
            msgs = res["messages"]
            text = str(msgs[-1].content)
            evidence = "\n".join(str(m.content) for m in msgs if isinstance(m, ToolMessage))
        except GraphRecursionError:
            text = "THIẾU: vượt giới hạn số lần gọi công cụ"
        except Exception as e:
            text = f"THIẾU: lỗi khi thực thi ({e})"
        if "THIẾU" not in text:
            break
    return task["id"], {"goal": task["goal"], "text": text, "evidence": evidence}


def execute_node(state: PlanState, retriever, llm_client: LLMClient, plan_client: LLMClient | None = None) -> dict:
    print(">>> [LP] execute")
    w = state["lp_window"]
    tools = {t.name: t for t in make_lp_tools(retriever, plan_client or llm_client, state["student_model"], w["subject"], w)
             + make_planning_tools(retriever, llm_client)}
    results = dict(state.get("lp_results", {}))
    pending = [t for t in state["lp_tasks"] if t["id"] not in results]

    while pending:
        ready = [t for t in pending if all(d in results for d in t["depends_on"])] or pending[:1]
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            for tid, r in list(ex.map(lambda t: _run_task(t, tools, state, llm_client, results), ready)):
                results[tid] = r
        pending = [t for t in pending if t["id"] not in results]
    knowledge = {c: k for c in w["chapter_ids"] if (k := _load_cache(w["subject"], c))}     # cache -> state, một lần
    return {"lp_results": results, "lp_knowledge": knowledge, "current_step": "learning_path"}