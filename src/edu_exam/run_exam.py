import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
# from graph import exam_graph
from langgraph.graph import StateGraph, END
from src.clients.llm import LLMClient

from src.configs import env_config
# from state_edu import ExamState
from src.state_edu import ExamState
from langchain_core.runnables import RunnableConfig
from src.clients.embedding import embeddings_qa
from src.edu_exam.collect_info import collect_info
from src.edu_exam.build_knowledge import build_knowledge as _build_knowledge
from src.edu_exam.build_matrix import build_matrix as _build_matrix
from src.edu_exam.build_specs import build_specs as _build_specs
from src.edu_exam.generate_questions import generate_questions as _generate_questions
from src.edu_exam.evaluate_exam import evaluate_exam as _evaluate_exam
from src.edu_exam.retrieve_docs import retrieve_docs as _retrieve_docs
 
from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever

from functools import partial
load_dotenv()
 
def create_graph(llm_client: LLMClient,retriever):
    g = StateGraph(ExamState)
 
    g.add_node("collect_info",       partial(collect_info, llm_client=llm_client))
    g.add_node("retrieve_docs",      partial(_retrieve_docs, llm_client=llm_client, retriever=retriever, top_k=5))
    g.add_node("build_knowledge",    partial(_build_knowledge, llm_client=llm_client))
    g.add_node("build_matrix",       partial(_build_matrix, llm_client=llm_client))
    g.add_node("build_specs",        partial(_build_specs, llm_client=llm_client))
    g.add_node("generate_questions", partial(_generate_questions, llm_client=llm_client))
    g.add_node("evaluate_exam",      partial(_evaluate_exam, llm_client=llm_client))
 
    g.set_entry_point("collect_info")
 
    g.add_conditional_edges(
        "collect_info",
        lambda state: "retrieve_docs" if state.get("profile_complete") else END,
        {"retrieve_docs": "retrieve_docs", END: END}
    )
 
    g.add_conditional_edges(
        "retrieve_docs",
        lambda state: (
            "build_knowledge"
            if state.get("retrieve_complete")
            else END
        ),
        {
            "build_knowledge": "build_knowledge",
            END: END,
        }
    )
 
    g.add_conditional_edges(
        "build_knowledge",
        lambda state: "build_matrix" if state.get("knowledge_done") else END,
        {"build_matrix": "build_matrix", END: END}
    )    

    g.add_conditional_edges(
        "build_matrix",
        lambda state: "build_specs" if state.get("matrix_done") else END,
        {"build_specs": "build_specs", END: END}
    )

    g.add_conditional_edges(
        "build_specs",
        lambda state: "generate_questions" if state.get("specs_done") else END,
        {"generate_questions": "generate_questions", END: END}
    )
    
    # g.add_edge("build_specs",        "generate_questions")
    g.add_edge("generate_questions", "evaluate_exam")
    g.add_edge("evaluate_exam",      END)
 
    return g.compile()
 
 
def run():
    print("=" * 50)
    print("🎓 Hệ thống tạo đề kiểm tra thông minh")
    print("=" * 50)
    print("Gõ 'quit' để thoát\n")
 
    # llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)
    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)

 
    retriever = VectorStoreRetriever(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
        embeddings=embeddings_qa,
        collection_name="doc_toan_10_1",
        top_k=10,
    )
 
    graph = create_graph(llm_client, retriever)
 
    state = {
        "messages": [],
        "student_profile": {},
        "profile_complete": False,
        "detected_chapters": [],
        "retrieved_chunks": [],
        "retrieve_complete": False,
        "scope_chapters": {},
        "scope_lessons": {},
        "section_selected": False,
        "scored_chunks": [],
        "_pending_sections": [],
        "knowledge_profile": {},
        "knowledge_queue":   None,
        "knowledge_pending": None,
        "knowledge_scores":  {},
        "knowledge_done":    False,
        "completed_build_knowlege" : False,
        "exam_matrix": {},
        "question_specs": [],
        "specs_done": False,
        "generated_exam": [],
        "exam_memory": [],
        "generate_done":  False,
        "exam_review": {},
        "final_exam": [],
        "evaluate_done": False,
        "current_step": "",
        "error": None,
    }
 
    
    while True:
        user_input = input("Học sinh: ").strip()
        if user_input.lower() == "quit":
            break
        if not user_input:
            continue

        # bỏ # ở đầu mỗi dòng
        user_input = "\n".join(
            line.lstrip("#").strip()
            for line in user_input.splitlines()
        )
 
        state["messages"].append(HumanMessage(content=user_input))


        if not state.get("profile_complete"):
            state = graph.invoke(state)
        elif not state.get("knowledge_done"):
            state = graph.invoke(state)
        elif not state.get("matrix_done"):
            state = graph.invoke(state)
        elif not state.get("specs_done"):
            state = graph.invoke(state)
        elif not state.get("generate_done"):
            state = graph.invoke(state)
        elif not state.get("evaluate_done"):
            state = graph.invoke(state)
        else:
            break

        
        # In phản hồi AI mới nhất
        ai_messages = [m for m in state["messages"] if hasattr(m, "type") and m.type == "ai"]
        if ai_messages:
            print("-"*70)
            print(f"Trợ lý: {ai_messages[-1].content}\n")
            print("-"*70)
 

 
        if state.get("knowledge_done"):
            print(f"knowledge_done ====> TRUE")
        if state.get("specs_done"):
            print(f"specs_done     ====> TRUE")
        if state.get("generate_done"):
            print(f"generate_done  ====> TRUE")
        if state.get("evaluate_done"):
            print(f"evaluate_done  ====> TRUE")
 
 
    return state
 
 
if __name__ == "__main__":
    run()


# tôi cần tạo đề thi toán 10 , 10 câu trắc nghiệm trong 40 phút với mục tiêu 9 điểm để ôn thi cuối kì ,phạm vi 1 chương đầu tiên phần đại số ,chương 1 khá ,chú ý vào chương 1 , tôi xác nhận đúng

 
# tôi cần tạo đề thi toán 10 , 10 câu trắc nghiệm trong 40 phút với mục tiêu 9 điểm để ôn thi cuối kì ,phạm vi 3 chương đầu tiên phần đại số ,chương 1 khá , chương 2 giỏi, chương 3 mức 8 điểm ,chú ý vào chương 1 và 3 , tôi xác nhận đúng
# 1,0,2,0,2,1,0,2,0,3
# 2,0,3,0,0,3
# 1,2,1,2,3,1,3

# python -m uvicorn src.api.main:app --reload --port 8000

# Đồng ý, batch là đúng hướng — 50 lần gọi LLM riêng lẻ chỉ để chọn tool là quá lãng phí. Nhưng có 1 ràng buộc kỹ thuật cần nói rõ trước:

# **Vấn đề:** cách cũ (`llm_with_tools = llm_client._llm.bind_tools(candidate_tools); response.tool_calls`) là cơ chế **function-calling gốc của LangChain** — chỉ thiết kế cho **1 câu hỏi → 1 lần gọi tool** trong 1 lượt invoke, không hỗ trợ "chọn N tool khác nhau cho N câu khác nhau trong cùng 1 lần gọi". Muốn batch, phải **đổi cơ chế**: không dùng `bind_tools` nữa, mà dùng `with_structured_output` — LLM chỉ trả về **dữ liệu** (chọn tool nào, tham số gì) cho từng câu, còn việc **thực thi tool thật sự** thì code Python tự làm sau (không qua LangChain tool-call).

# Đây là điểm khác với `qa_solve_agent.py` bạn từng bảo tham khảo (file đó xử lý per-question nên dùng `bind_tools` được) — giờ đổi kiến trúc để batch được.

# ### File: `state_edu.py` (thêm schema)

# ```python
# from typing import Any

# class ToolSelection(BaseModel):
#     id: int = Field(description="id câu hỏi tương ứng, PHẢI khớp đúng id trong danh sách câu hỏi đã cho")
#     tool_name: str = Field(description="Tên tool được chọn — PHẢI đúng 1 trong danh sách tool khả dụng, hoặc 'khong_co_tool_phu_hop' nếu không tool nào khớp dạng bài")
#     tool_args: Dict[str, Any] = Field(default_factory=dict, description="Tham số truyền vào tool đã chọn, đúng tên tham số theo mô tả tool, lấy giá trị từ chính dữ kiện trong câu hỏi")

# class ToolSelectionBatch(BaseModel):
#     selections: List[ToolSelection]
# ```

# ---

# ### File: `qa_solve_tool_select_batch_prompt.txt` (mới — thay cho việc dùng `bind_tools`)

# ```
# Bạn là trợ lý chọn công cụ tính toán phù hợp cho từng câu hỏi Toán 10.

# DANH SÁCH TOOL KHẢ DỤNG (tên và mô tả "Dùng khi...")
# {tool_reference}

# DANH SÁCH CÂU HỎI CẦN CHỌN TOOL
# {questions}

# NHIỆM VỤ
# Với MỖI câu hỏi, chọn đúng 1 tool phù hợp nhất trong danh sách trên, dựa vào mô tả "Dùng khi..." của từng tool, rồi điền tham số cho tool đó dựa theo đúng dữ kiện có trong câu hỏi.
# Nếu không tool nào trong danh sách phù hợp với câu hỏi, đặt tool_name = "khong_co_tool_phu_hop" và tool_args rỗng.
# Không bịa thêm dữ kiện ngoài câu hỏi đã cho. id trong kết quả PHẢI khớp đúng id câu hỏi tương ứng, không thiếu không thừa.
# ```

# ---

# ### File: `evaluate_exam.py` (thay `_verify_bai_tap_with_tools` + hàm phụ)

# ```python
# from typing import Any
# from src.state_edu import ToolSelection, ToolSelectionBatch

# TOOL_VERIFY_BATCH_SIZE  = 8
# TOOL_SELECT_BATCH_PROMPT_PATH = Path(r'...\qa_solve_tool_select_batch_prompt.txt')


# def _select_candidate_tools_for(retriever, question: str) -> list:
#     """Retrieval THUẦN (không LLM) — lấy tool ứng viên cho 1 câu, cascade threshold 0.6/0.4."""
#     docs     = retriever.hybrid_search_tools(question, k=15)
#     reranked = retriever.rerank(question, docs, top_k=TOOLS_TOP_K)
#     filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_1]
#     if not filtered:
#         filtered = [d for d in reranked if d.metadata.get("rerank_score", 0) >= TOOLS_SCORE_THRESHOLD_2]
#     return [d.metadata.get("tool_name") for d in filtered if d.metadata.get("tool_name") in TOOL_MAP_V2]


# def _format_tool_reference(tool_names: set) -> str:
#     return "\n".join(f"- {name}: {TOOL_MAP_V2[name].description}" for name in sorted(tool_names))


# def _format_questions_for_tool_batch(questions: list) -> str:
#     return "\n".join(f"id={q['id']} | question: {q['question']}" for q in questions)


# def _verify_bai_tap_with_tools(generated_exam: list, retriever, llm_client: LLMClient) -> None:
#     bai_tap_questions = [q for q in generated_exam if q.get("type") == "bai_tap"]
#     if not bai_tap_questions:
#         return

#     template = TOOL_SELECT_BATCH_PROMPT_PATH.read_text(encoding="utf-8")

#     for i in range(0, len(bai_tap_questions), TOOL_VERIFY_BATCH_SIZE):
#         batch = bai_tap_questions[i:i + TOOL_VERIFY_BATCH_SIZE]

#         # Retrieval từng câu (không LLM) → gộp tool ứng viên của cả batch
#         candidate_per_q = {q["id"]: _select_candidate_tools_for(retriever, q["question"]) for q in batch}
#         union_tools = set(t for tools in candidate_per_q.values() for t in tools)

#         if not union_tools:
#             for q in batch:
#                 q["tool_used"], q["answer_tools"], q["mapping"] = None, "Không tìm được tool phù hợp", "❌"
#             continue

#         prompt = (template
#                   .replace("{tool_reference}", _format_tool_reference(union_tools))
#                   .replace("{questions}", _format_questions_for_tool_batch(batch)))

#         result = llm_client.invoke_structured(ToolSelectionBatch, [{"role": "user", "content": prompt}])
#         selections_by_id = {s.id: s for s in result.selections} if result else {}

#         for q in batch:
#             sel = selections_by_id.get(q["id"])
#             if not sel or sel.tool_name not in TOOL_MAP_V2:
#                 q["tool_used"], q["answer_tools"], q["mapping"] = None, "LLM không chọn được tool hợp lệ", "❌"
#                 continue

#             try:
#                 output = TOOL_MAP_V2[sel.tool_name].invoke(sel.tool_args)
#             except Exception as e:
#                 output = f"LOI: {e}"

#             q["tool_used"]    = sel.tool_name
#             q["answer_tools"] = output

#             if isinstance(output, str) and output.startswith("LOI:"):
#                 q["mapping"] = "❌"
#             else:
#                 chosen_text = q.get("options", {}).get(q.get("answer", ""), "")
#                 q["mapping"] = "✅" if _check_mapping(output, chosen_text) else "❌"
# ```

# Bỏ hẳn `_select_and_call_tool` (bản `bind_tools` cũ) — không dùng nữa.

# ---

# **Kết quả với ví dụ 50 câu `bai_tap`, `TOOL_VERIFY_BATCH_SIZE=8`:**

# ```
# ceil(50/8) = 7 lần gọi LLM   (thay vì 50 lần)
# ```

# Retrieval (`hybrid_search_tools`+`rerank`) vẫn chạy **50 lần** (không đổi, vì đây không phải LLM call, chỉ là embedding+cross-encoder — rẻ hơn nhiều) để đảm bảo mỗi câu vẫn có candidate tool riêng sát đúng, gộp lại mới đưa vào 1 batch.

# **Đánh đổi cần biết:** prompt mỗi batch giờ lớn hơn (liệt kê union tool + 8 câu hỏi cùng lúc thay vì 1 câu), nhưng tổng token vẫn giảm mạnh so với 50 lần gọi riêng (mỗi lần đều phải trả phí "khởi động" system prompt/tool schema).

# Bạn thấy `TOOL_VERIFY_BATCH_SIZE=8` ổn không, hay muốn chỉnh con số khác (batch lớn hơn = ít call hơn nhưng rủi ro model nhầm lẫn giữa các câu tăng)?