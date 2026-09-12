from typing import Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class SubQuery(BaseModel):
    id: str = Field(..., description="ID của sub-query, VD: '1', '2', '1.1' nếu là câu hỏi con của câu 1")
    text: str = Field(..., description="vấn đề đã được viết lại rõ ràng, tách nhỏ nếu câu gốc chứa nhiều ý, giữ đúng nội dung bài toán gốc (số liệu, dữ kiện)")
    retrieval_query: str = Field(..., description="Câu query viết lại theo văn phong LÝ THUYẾT/KHÁI NIỆM (không chứa số liệu cụ thể của bài), dùng để tìm kiếm trong sách giáo khoa, VD: 'Phép giao của hai tập hợp' thay vì 'Tính A giao B với A={1,2,3}'")
    chapter_hint: Optional[str] = Field(default=None, description="chủ đề chương/bài học liên quan nếu nhận diện được từ câu hỏi, VD: 'Chương 1 Mệnh Đề', 'Bài 2 hàm số'")

class RouterOutput(BaseModel):
    valid: Literal[0, 1] = Field(..., description="0 = câu hỏi lệch đủ đề/mơ hồ cần làm rõ, 1 = câu hỏi hợp lệ,liên quan chủ để học tập, hỏi đáp kiến thức, giải thích bài học về lý thuyết/bài tập các môn Toán 10, Ngữ văn 10, Lịch sử 10")
    ly_do: str = Field(..., description="Giải thích ngắn gọn vì sao chọn valid như vậy")
    subject: Optional[Literal["Toán 10", "Ngữ văn 10", "Lịch sử 10"]] = Field(default=None, description="Môn học được phân loại từ vấn đề người dùng yêu cầu, chỉ có giá trị khi valid=1")
    query_type: Optional[Literal["ly_thuyet", "bai_tap"]] = Field(default=None, description="Loại câu hỏi:chỉ lý thuyết hoặc bài tập/thực hành, bai tập yêu cầu sự logic tính toán áp dụng công thức hay các biểu thức,  chỉ có giá trị khi valid=1")
    sub_queries: list[SubQuery] = Field(default_factory=list, description="Danh sách câu hỏi con cần tách nhỏ khi vấn đề quá phức tạp và bao hàm nhiều ẩn lý và nội dung có sự phân tách, rỗng nếu valid=0")
    clarify_question: Optional[str] = Field(default=None, description="Câu hỏi lại cho người dùng nếu cần làm rõ ý định hay chưa đủ thông tin cơ sở khẳng định vấn đề, chỉ khi valid=0")


class RetrievedChunk(BaseModel):
    chunk_id: Optional[str] = Field(default=None, description="ID duy nhất của chunk trong metadata, dùng để dedupe")
    content: str = Field(..., description="phần nội dung chứa dữ liệu liên quan đến vấn đề người dùng đề cập , được dùng làm tài liệu tham khảo để trả lời các câu hỏi")
    source: str = Field(..., description="Tên tài liệu nguồn, VD: 'kho dữ liệu' , 'internet','sách giáo khoa Toán 10'")
    chapter: Optional[str] = Field(default=None, description="Chương/bài/ chủ đề của tài liệu có thể chứa ở metadata hoặc content")
    score: float = Field(..., description="Điểm relevance sau khi rerank, càng cao càng liên quan đến vấn đề cẩn giải quyết")


class RagResult(BaseModel):
    sub_query_id: str = Field(..., description="ID của sub-query tương ứng, khớp với SubQuery.id")
    chunks: list[RetrievedChunk] = Field(..., description="Danh sách chunk đã retrieve và rerank cho sub-query này")
    is_sufficient: bool = Field(..., description="True nếu dữ liệu đã đủ để trả lời, False nếu cần retrieve thêm")
    answer: Optional[str] = Field(default=None, description="Câu trả lời cho sub-query này, có giá trị khi is_sufficient=True")
    retrieve_round: int = Field(default=1, description="Số vòng đã retrieve cho sub-query này, tối đa 2")
    used_web: bool = Field(default=False, description="True nếu câu trả lời phải dùng fallback web search do dữ liệu nội bộ không đủ")
    
class SolveResult(BaseModel):
    sub_query_id: str = Field(..., description="ID của sub-query tương ứng cần tính toán")
    tool_used: str = Field(..., description="Tên tool tính toán đã dùng, hoặc 'none' nếu không đủ dữ kiện")
    tool_input: Optional[dict] = Field(default=None, description="Tham số đã truyền vào tool")
    result: str = Field(..., description="Kết quả thô trả về từ tool, hoặc 'chưa đủ dữ kiện'")
    steps: Optional[str] = Field(default=None, description="Quy trình tính toán dẫn tới kết quả, dựa trên query, context và tool đã dùng")
    # context_source: str = Field(default="rag", description="Nguồn context dùng để giải: 'rag' hoặc 'web_search'")
    context_source: Literal["internal", "web", "none"] = Field(default="internal", description="Nguồn context dùng để giải: 'internal' (Qdrant doc_final), 'web' (web search fallback), 'none' (không có context)")
    verify_method: Literal["tool", "llm_fallback"] = Field(default="tool", description="'tool' nếu dùng SymPy tool tính toán, 'llm_fallback' nếu không có tool phù hợp và LLM tự suy luận trực tiếp")

class LLMFallbackAnswer(BaseModel):
    quy_trinh: str = Field(..., description="Quá trình suy luận, giải thích từng bước tính toán dẫn tới kết quả cuối cùng")
    ket_qua: str = Field(..., description="Kết quả cuối cùng, ngắn gọn, cùng định dạng với kết quả 1 tool tính toán trả về")
    
class SubAnswer(BaseModel):
    sub_query_id: str = Field(..., description="ID sub-query tương ứng, khớp SubQuery.id")
    sub_query_text: str = Field(..., description="Nội dung câu hỏi (copy lại từ SubQuery.text) để dễ đối chiếu, chỉ mang tính hiển thị")
    answer: str = Field(..., description="Câu trả lời cho sub-query này, hoặc câu thông báo chưa đủ dữ kiện")

class KnowledgeAnswerOutput(BaseModel):
    answers: list[SubAnswer] = Field(..., description="Danh sách câu trả lời, đúng thứ tự và đủ số lượng sub_queries đã hỏi")

class ChatTurn(BaseModel):
    user_query: str = Field(..., description="Câu hỏi của học sinh ở lượt này")
    final_answer: str = Field(..., description="Câu trả lời hệ thống đã đưa ra cho lượt này")

class FormattedAnswer(BaseModel):
    final_answer: str = Field(..., description="Câu trả lời hoàn chỉnh với văn phong tự nhiên, đã gộp các các câu trả lời theo từng ý nếu có, không thêm/bớt thông tin ngoài kết quả được cung cấp")
    suggestions: list[str] = Field(default_factory=list, description="1-3 câu hỏi gợi ý tiếp theo liên quan đến chủ đề đang thảo luận, dựa trên nội dung câu hỏi , câu trả lời và nội dung cuộc trò chuyện")
    
class QAState(BaseModel):
    user_query: str = Field(..., description="vấn đề hiện tại mà người dùng đang đề cập, có thể là câu hỏi, yêu cầu giải thích, hay bài tập cần tính toán")
    chat_history: list[ChatTurn] = Field(default_factory=list, description="Lịch sử hỏi đáp các lượt trước trong cùng phiên trò chuyện, dùng để hiểu ngữ cảnh lịch sử, chủ đề đang thảo luận, rất quan trong để xác định ý định vấn đề ngay lúc này")
    router_output: Optional[RouterOutput] = Field(default=None, description="Kết quả suy luận phân loại từ qa_router_agent")
    rag_results: list[RagResult] = Field(default_factory=list, description="Kết quả retrieve theo từng sub-query, có khi query_type='ly_thuyet'")
    solve_results: list[SolveResult] = Field(default_factory=list, description="Kết quả tính toán, chỉ có khi subject='Toán 10' và query_type='bai_tap'")
    final_answer: Optional[str] = Field(default=None, description="Câu trả lời cuối cùng đã trâu chuốc chuẩn chỉ , trả về cho người dùng về vấn đề hiện tại hoặc thông báo trong cuộc trò chuyện")
    suggestions: list[str] = Field(default_factory=list, description="Câu hỏi gợi ý tiếp theo liên quan đến chủ đề trò chuyện, sinh ra cùng lúc với final_answer")
    query_timestamp: Optional[datetime] = Field(default=None, description="Thời điểm hệ thống nhận câu hỏi từ người dùng")