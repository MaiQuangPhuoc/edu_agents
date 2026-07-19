import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from typing import Literal, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document

from src.clients.llm import LLMClient
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
from src.edu_qa.state import QAState, SolveResult
from src.edu_qa.paths import PROMPT_DIR
from src.edu_qa.tools.web_search_tool import web_search_math
from src.edu_qa.tools.sympy_qa_tools import (
    sympy_diff, sympy_solve, sympy_simplify, sympy_evaluate,
)
from src.edu_qa.tools.set_tools import set_union, set_intersection, set_difference, is_subset
from src.edu_qa.tools.inequality_tools import check_point_in_region, linear_optimize
from src.edu_qa.tools.quadratic_tools import quadratic_vertex, quadratic_sign

TOOL_SELECT_PROMPT_PATH = PROMPT_DIR / "qa_solve_tool_select_prompt.txt"
PROCESS_PROMPT_PATH = PROMPT_DIR / "qa_solve_process_prompt.txt"
WEB_SUMMARIZE_PROMPT_PATH = PROMPT_DIR / "qa_solve_web_summarize_prompt.txt"

WEB_RERANK_THRESHOLD = 0.7
INSUFFICIENT_MARKER = "thiếu thông tin"
CANNOT_SUMMARIZE_MARKER = "khong the tom luoc"

TOOL_MAP = {
    "sympy_diff": sympy_diff,
    "sympy_solve": sympy_solve,
    "sympy_simplify": sympy_simplify,
    "sympy_evaluate": sympy_evaluate,
    "set_union": set_union,
    "set_intersection": set_intersection,
    "set_difference": set_difference,
    "is_subset": is_subset,
    "check_point_in_region": check_point_in_region,
    "linear_optimize": linear_optimize,
    "quadratic_vertex": quadratic_vertex,
    "quadratic_sign": quadratic_sign,
}

TOOL_NAME_LITERAL = Literal[
    "sympy_diff", "sympy_solve", "sympy_simplify", "sympy_evaluate",
    "set_union", "set_intersection", "set_difference", "is_subset",
    "check_point_in_region", "linear_optimize",
    "quadratic_vertex", "quadratic_sign",
]


class ToolSelection(BaseModel):
    tool_name: TOOL_NAME_LITERAL = Field(..., description="Tên tool cần gọi, khớp chính xác 1 trong 12 tool đã liệt kê")
    kwargs: dict = Field(..., description="Các tham số cần truyền vào tool dưới dạng key-value, đúng tên tham số của tool đó")


class SolveOutput(BaseModel):
    ket_qua: str = Field(..., description="Kết quả cuối cùng, chỉ chứa đáp số, không kèm diễn giải")
    cac_buoc: str = Field(..., description="Diễn giải các bước tính toán dẫn tới kết quả")

class SolveProcess(BaseModel):
    steps: str = Field(..., description="Quy trình các bước tính toán, dựa đúng theo tool đã gọi và kết quả tool trả về")

class WebSummary(BaseModel):
    summary: str = Field(..., description="Nội dung lý thuyết/công thức đã tóm lược, hoặc 'khong the tom luoc' nếu không dùng được")


# ── Lấy context: ưu tiên rag, fallback web search ───────────────────────────

def _get_rag_answer(state: QAState, sub_query_id: str) -> Optional[str]:
    rag = next((r for r in state.rag_results if r.sub_query_id == sub_query_id), None)
    if rag and rag.is_sufficient and rag.answer:
        return rag.answer
    return None


def _web_results_to_documents(results: list[dict]) -> list[Document]:
    return [
        Document(page_content=r["content"], metadata={"title": r["title"], "url": r["url"]})
        for r in results
    ]


async def _summarize_web_context(question: str, web_context: str, llm_client: LLMClient) -> WebSummary:
    template = WEB_SUMMARIZE_PROMPT_PATH.read_text(encoding="utf-8")
    prompt_text = template.format(question=question, web_context=web_context)
    messages = [HumanMessage(content=prompt_text)]

    result: WebSummary = await llm_client.ainvoke_with_retries(
        prompt=messages, output_model=WebSummary, temperature=0.0,
    )
    return result


async def _get_context_via_web(
    question: str, retriever: VectorStoreRetriever, llm_client: LLMClient,
) -> tuple[Optional[str], str]:
    """Trả về (context hoặc None, context_source)."""
    web_results = web_search_math.invoke({"query": question})
    if not web_results:
        return None, "web_search"

    web_docs = _web_results_to_documents(web_results)
    reranked = retriever.rerank(question, web_docs, top_k=3)

    if not reranked or reranked[0].metadata.get("rerank_score", 0.0) < WEB_RERANK_THRESHOLD:
        return None, "web_search"

    web_context = "\n---\n".join(d.page_content for d in reranked)
    summary = await _summarize_web_context(question, web_context, llm_client)

    if summary.summary.strip().lower() == CANNOT_SUMMARIZE_MARKER:
        return None, "web_search"

    return summary.summary, "web_search"


# ── Chọn tool, gọi tool ──────────────────────────────────────────────────────

async def _select_tool(question: str, rag_answer: str, llm_client: LLMClient) -> ToolSelection:
    template = TOOL_SELECT_PROMPT_PATH.read_text(encoding="utf-8")
    prompt_text = template.format(question=question, rag_answer=rag_answer)
    messages = [HumanMessage(content=prompt_text)]

    result: ToolSelection = await llm_client.ainvoke_with_retries(
        prompt=messages, output_model=ToolSelection, temperature=0.0,
    )
    return result


def _call_tool(selection: ToolSelection) -> str:
    tool_fn = TOOL_MAP[selection.tool_name]
    return tool_fn.invoke(selection.kwargs)


async def _describe_process(
    question: str, context: str, selection: ToolSelection, tool_output: str, llm_client: LLMClient,
) -> SolveProcess:
    template = PROCESS_PROMPT_PATH.read_text(encoding="utf-8")
    prompt_text = template.format(
        question=question,
        context=context,
        tool_name=selection.tool_name,
        tool_input=str(selection.kwargs),
        tool_output=tool_output,
    )
    messages = [HumanMessage(content=prompt_text)]

    result: SolveProcess = await llm_client.ainvoke_with_retries(
        prompt=messages, output_model=SolveProcess, temperature=0.0,
    )
    return result


# ── Node chính ───────────────────────────────────────────────────────────────

async def run_qa_solve_agent(
    state: QAState,
    llm_client: LLMClient,
    retriever: VectorStoreRetriever,
) -> QAState:
    solve_results = []

    for q in state.router_output.sub_queries:
        context = _get_rag_answer(state, q.id)
        context_source = "rag"

        if context is None:
            context, context_source = await _get_context_via_web(q.text, retriever, llm_client)

        if context is None:
            solve_results.append(SolveResult(
                sub_query_id=q.id,
                tool_used="none",
                tool_input=None,
                result="chưa đủ dữ kiện",
                steps=None,
                context_source=context_source,
            ))
            continue

        selection = await _select_tool(q.text, context, llm_client)
        tool_output = _call_tool(selection)
        process = await _describe_process(q.text, context, selection, tool_output, llm_client)

        solve_results.append(SolveResult(
            sub_query_id=q.id,
            tool_used=selection.tool_name,
            tool_input=selection.kwargs,
            result=tool_output,
            steps=process.steps,
            context_source=context_source,
        ))

    state.solve_results = solve_results
    return state
print("QA solve agent built successfully")