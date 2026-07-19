from typing import Literal, Optional
from pydantic import BaseModel, Field


class SubQuery(BaseModel):
    id: str = Field(..., description="ID của sub-query, VD: '1', '2', '1.1' nếu là câu hỏi con của câu 1")
    text: str = Field(..., description="Câu query đã được viết lại rõ ràng, tách nhỏ nếu câu gốc chứa nhiều ý, VD: 'Đạo hàm là gì', 'Vì sao hàm số bậc nhất đồng biến khi a>0'")
    chapter_hint: Optional[str] = Field(default=None, description="Gợi ý chương/bài liên quan nếu nhận diện được từ câu hỏi, VD: 'Chương 1', 'Bài đạo ôn'")


class RouterOutput(BaseModel):
    loai: Literal[1, 2, 3] = Field(..., description="Phân loại câu hỏi: 1 = mơ hồ cần hỏi lại, 2 = câu hỏi lý thuyết, 3 = câu hỏi cần tính toán")
    ly_do: str = Field(..., description="Giải thích ngắn gọn vì sao phân loại như vậy")
    sub_queries: list[SubQuery] = Field(default_factory=list, description="Danh sách câu hỏi con đã tách nhỏ, rỗng nếu loai=1")
    clarify_question: Optional[str] = Field(default=None, description="Câu hỏi lại cho user để làm rõ ý định, chỉ có giá trị khi loai=1")


class RetrievedChunk(BaseModel):
    content: str = Field(..., description="Nội dung đoạn văn bản được truy xuất từ vectorDB")
    source: str = Field(..., description="Tên tài liệu nguồn, VD: 'dao_on.docx'")
    chapter: Optional[str] = Field(default=None, description="Chương/bài của chunk này nếu có metadata")
    score: float = Field(..., description="Điểm relevance sau khi rerank, càng cao càng liên quan")


class RagResult(BaseModel):
    sub_query_id: str = Field(..., description="ID của sub-query tương ứng, khớp với SubQuery.id")
    chunks: list[RetrievedChunk] = Field(..., description="Danh sách chunk đã retrieve và rerank cho sub-query này")
    is_sufficient: bool = Field(..., description="True nếu dữ liệu đã đủ để trả lời, False nếu cần retrieve thêm")
    answer: Optional[str] = Field(default=None, description="Câu trả lời cho sub-query này, có giá trị khi is_sufficient=True")
    retrieve_round: int = Field(default=1, description="Số vòng đã retrieve cho sub-query này, tối đa 2")


class SolveResult(BaseModel):
    sub_query_id: str = Field(..., description="ID của sub-query tương ứng cần tính toán")
    tool_used: str = Field(..., description="Tên tool tính toán đã dùng, hoặc 'none' nếu không đủ dữ kiện")
    tool_input: Optional[dict] = Field(default=None, description="Tham số đã truyền vào tool")
    result: str = Field(..., description="Kết quả thô trả về từ tool, hoặc 'chưa đủ dữ kiện'")
    steps: Optional[str] = Field(default=None, description="Quy trình tính toán dẫn tới kết quả, dựa trên query, context và tool đã dùng")
    context_source: str = Field(default="rag", description="Nguồn context dùng để giải: 'rag' hoặc 'web_search'")


class ChatTurn(BaseModel):
    user_query: str = Field(..., description="Câu hỏi của học sinh ở lượt này")
    final_answer: str = Field(..., description="Câu trả lời hệ thống đã đưa ra cho lượt này")


class QAState(BaseModel):
    user_query: str = Field(..., description="Câu hỏi hiện tại của người dùng")
    chat_history: list[ChatTurn] = Field(default_factory=list, description="Lịch sử hỏi-đáp các lượt trước trong cùng phiên, dùng để hiểu ngữ cảnh câu hỏi hiện tại")
    router_output: Optional[RouterOutput] = Field(default=None, description="Kết quả phân loại từ qa_router_agent")
    rag_results: list[RagResult] = Field(default_factory=list, description="Kết quả retrieve theo từng sub-query")
    solve_results: list[SolveResult] = Field(default_factory=list, description="Kết quả tính toán, chỉ có khi loai=3")
    final_answer: Optional[str] = Field(default=None, description="Câu trả lời cuối cùng đã format, trả về user")