import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from src.clients.llm import LLMClient
from src.edu_qa.state import QAState, SolveResult
from src.edu_qa.paths import PROMPT_DIR
from src.edu_qa.tools.math_tools import MATH_TOOLS, algebra_tool, set_tool, linear_inequality_tool, quadratic_tool

TOOL_SELECT_PROMPT_PATH = PROMPT_DIR / "qa_solve_tool_select_prompt.txt"
PROCESS_PROMPT_PATH = PROMPT_DIR / "qa_solve_process_prompt.txt"

NO_ANSWER_MARKER = "Không biết"
INSUFFICIENT_RESULT = "chưa đủ dữ kiện"

TOOL_MAP = {
    "algebra_tool": algebra_tool,
    "set_tool": set_tool,
    "linear_inequality_tool": linear_inequality_tool,
    "quadratic_tool": quadratic_tool,
}


class SolveProcess(BaseModel):
    steps: str = Field(..., description="Quy trình các bước tính toán, dựa đúng theo tool đã gọi và kết quả tool trả về")


def _get_rag_answer(state: QAState, sub_query_id: str) -> Optional[str]:
    rag = next((r for r in state.rag_results if r.sub_query_id == sub_query_id), None)
    if rag and rag.answer and rag.answer != NO_ANSWER_MARKER:
        return rag.answer
    return None


async def _select_and_call_tool(question: str, context: str, llm_client: LLMClient):
    """Gọi LLM với bind_tools, LLM tự chọn tool + điền tham số đúng schema, trả về (tool_name, tool_args, tool_output)."""
    template = TOOL_SELECT_PROMPT_PATH.read_text(encoding="utf-8")
    prompt_text = template.format(question=question, context=context)
    messages = [HumanMessage(content=prompt_text)]

    llm_with_tools = llm_client._llm.bind_tools(MATH_TOOLS)
    response = await llm_with_tools.ainvoke(messages)
    print(f"LLM tool selection response: {response}")

    if not response.tool_calls:
        return None, None, "LOI: LLM khong goi tool nao"

    tool_call = response.tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    tool_fn = TOOL_MAP.get(tool_name)
    print(f"Calling tool: {tool_name} \nwith args: {tool_args}\n tool_fn  :{tool_fn}")
    if not tool_fn:
        return tool_name, tool_args, f"LOI: khong tim thay tool {tool_name}"

    tool_output = tool_fn.invoke(tool_args)
    print(f"Tool output: {tool_output}")
    return tool_name, tool_args, tool_output


async def _describe_process(
    question: str, context: str, tool_name: str, tool_args: dict, tool_output: str, llm_client: LLMClient,
) -> SolveProcess:
    template = PROCESS_PROMPT_PATH.read_text(encoding="utf-8")
    prompt_text = template.format(
        question=question,
        context=context,
        tool_name=tool_name,
        tool_input=str(tool_args),
        tool_output=tool_output,
    )
    messages = [HumanMessage(content=prompt_text)]

    result: SolveProcess = await llm_client.ainvoke_with_retries(
        prompt=messages, output_model=SolveProcess, temperature=0.0,
    )
    print(f"LLM process description response: {result}")
    return result


async def run_qa_solve_agent(state: QAState, llm_client: LLMClient) -> QAState:
    solve_results = []

    for q in state.router_output.sub_queries:
        context = _get_rag_answer(state, q.id)

        if context is None:
            solve_results.append(SolveResult(
                sub_query_id=q.id,
                tool_used="none",
                tool_input=None,
                result=INSUFFICIENT_RESULT,
                steps=None,
                context_source="none",
            ))
            continue

        tool_name, tool_args, tool_output = await _select_and_call_tool(q.text, context, llm_client)

        if tool_name is None or (isinstance(tool_output, str) and tool_output.startswith("LOI:")):
            solve_results.append(SolveResult(
                sub_query_id=q.id,
                tool_used=tool_name or "none",
                tool_input=tool_args,
                result=tool_output or INSUFFICIENT_RESULT,
                steps=None,
                context_source="rag",
            ))
            continue

        process = await _describe_process(q.text, context, tool_name, tool_args, tool_output, llm_client)

        solve_results.append(SolveResult(
            sub_query_id=q.id,
            tool_used=tool_name,
            tool_input=tool_args,
            result=tool_output,
            steps=process.steps,
            context_source="rag",
        ))
        
    print("============================ QA Solve Agent Output ============================")
    for res in solve_results:
        print(f"sub_query_id: {res.sub_query_id}, tool_used: {res.tool_used}, result: {res.result}, steps: {res.steps}\n----------\n")

    state.solve_results = solve_results
    return state