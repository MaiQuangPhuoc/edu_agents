import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.messages import HumanMessage

from src.clients.llm import LLMClient
from src.edu_qa.state import QAState, SolveResult
from src.edu_qa.paths import SOLVE_TOOL_SELECT_PROMPT_PATH
from src.edu_qa.tools.math_tools_v2 import TOOL_MAP_V2
from src.edu_qa.qa_knowledge_agent import answer_subquery_as_theory
from src.edu_qa.qa_memory import build_history_text

TOOLS_TOP_K = 3
TOOLS_SCORE_THRESHOLD_1 = 0.6
TOOLS_SCORE_THRESHOLD_2 = 0.4


def _select_candidate_tools(retriever, query: str) -> list:
    """Rerank top-3 tool cho câu hỏi trong collection 'tools', cascade threshold 0.6 -> 0.4.
    Trả về list tool object (rỗng nếu không tool nào đạt ngưỡng dù đã hạ threshold)."""
    docs = retriever.hybrid_search_tools(query, k=15)
    reranked = retriever.rerank(query, docs, top_k=TOOLS_TOP_K)

    filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_1]
    if not filtered:
        filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_2]

    tool_names = [d.metadata.get("tool_name") for d in filtered]
    tools = [TOOL_MAP_V2[name] for name in tool_names if name in TOOL_MAP_V2]
    return tools


async def _select_and_call_tool(question: str, retriever, llm_client: LLMClient):
    """Rerank chọn candidate tool, LLM đọc docstring chọn 1 tool + điền tham số, gọi tool.
    Trả về (tool_name, tool_args, output, co_tool: bool)."""
    candidate_tools = _select_candidate_tools(retriever, question)

    if not candidate_tools:
        return None, None, None, False

    template = SOLVE_TOOL_SELECT_PROMPT_PATH.read_text(encoding="utf-8")
    prompt_text = template.format(question=question)
    messages = [HumanMessage(content=prompt_text)]

    llm_with_tools = llm_client._llm.bind_tools(candidate_tools)
    response = await llm_with_tools.ainvoke(messages)
    print(f"LLM tool selection response: {response}")

    if not response.tool_calls:
        return None, None, None, False

    tool_call = response.tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    tool_fn = TOOL_MAP_V2.get(tool_name)
    if not tool_fn:
        return tool_name, tool_args, None, False

    tool_output = tool_fn.invoke(tool_args)
    print(f"Tool output: {tool_output}")

    if isinstance(tool_output, str) and tool_output.startswith("LOI:"):
        return tool_name, tool_args, None, False

    return tool_name, tool_args, tool_output, True


async def run_qa_solve_agent(state: QAState, retriever, llm_client: LLMClient) -> QAState:
    print("================== qa_solve_agent.py ================== ")
    router_output = state.router_output
    assert router_output.subject == "Toán 10" and router_output.query_type == "bai_tap", (
        f"qa_solve_agent chỉ xử lý subject='Toán 10' và query_type='bai_tap', "
        f"nhận được subject='{router_output.subject}', query_type='{router_output.query_type}'"
    )

    chat_history_text = build_history_text(state)
    solve_results = []

    for sq in router_output.sub_queries:
        tool_name, tool_args, output, co_tool = await _select_and_call_tool(sq.text, retriever, llm_client)

        if co_tool:
            solve_results.append(SolveResult(
                sub_query_id=sq.id,
                tool_used=tool_name,
                tool_input=tool_args,
                result=str(output),
                steps=None,
                context_source="none",
                verify_method="tool",
            ))
        else:
            answer, chunks, used_web = await answer_subquery_as_theory(
                sq, "Toán 10", chat_history_text, retriever, llm_client
            )
            solve_results.append(SolveResult(
                sub_query_id=sq.id,
                tool_used=tool_name or "none",
                tool_input=tool_args,
                result=answer,
                steps=None,
                context_source="web" if used_web else ("internal" if chunks else "none"),
                verify_method="llm_fallback",
            ))

    state.solve_results = solve_results

    print("============================ QA Solve Agent Output ============================")
    for res in solve_results:
        print(f"sub_query_id: {res.sub_query_id}, tool_used: {res.tool_used}, verify_method: {res.verify_method}, result: {res.result}\n----------\n")
    print("============================ QA Solve Agent Output ============================\n\n")

    return state

print("qa_solve_agent.py loaded successfully")