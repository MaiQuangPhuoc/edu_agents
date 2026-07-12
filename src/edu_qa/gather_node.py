import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pathlib import Path
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from src.edu_qa.qa_state import QAState, get_last_question
from src.clients.llm import LLMClient
from src.edu_qa.tools.qa_gather_tools import build_search_tool, build_clarify_tool

PROMPT_PATH = Path(r'D:\VKU\Nam_4\ky_I\computer_vision\EDUAGENT\prompt_edu\prompt\qa_gather_agent.txt')

# Giới hạn kỹ thuật (ngăn vòng lặp vô hạn khi agent lỗi), KHÔNG phải logic
# nghiệp vụ — agent vẫn tự quyết định có cần dùng hết giới hạn này không.
MAX_STEPS = 6


def gather_node(state: QAState, llm_client: LLMClient, retriever) -> dict:
    print(">>> [Node] gather_node")

    question = get_last_question(state)

    collected_docs: list = []
    outcome = {"awaiting_user": False, "clarify_question": None}

    search_tool  = build_search_tool(retriever, collected_docs)
    clarify_tool = build_clarify_tool(outcome)

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    agent = create_react_agent(
        model=llm_client._llm,
        tools=[search_tool, clarify_tool],
        prompt=system_prompt,
    )

    agent.invoke(
        {"messages": [HumanMessage(content=question)]},
        config={"recursion_limit": MAX_STEPS},
    )

    if outcome["awaiting_user"]:
        print(">>> gather_node: agent quyết định cần hỏi lại học sinh")
        return {
            "messages":         [AIMessage(content=outcome["clarify_question"])],
            "clarify_question": outcome["clarify_question"],
            "awaiting_user":    True,
            "retrieved_chunks": [],
        }

    chunks = [
        {"content": d.page_content, "metadata": d.metadata}
        for d in collected_docs
    ]
    print(f">>> gather_node: agent đã lấy {len(chunks)} chunk (0 nếu không cần retrieve)")

    return {
        "retrieved_chunks": chunks,
        "awaiting_user":    False,
    }
