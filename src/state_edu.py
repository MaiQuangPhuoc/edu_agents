from typing import Annotated, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages


# ── Schema bước 1: Hồ sơ học sinh ───────────────────────────────────────────

from pydantic import BaseModel, Field
from typing import Optional, List


class KnowledgeItem(BaseModel):
    """Một mục kiến thức học sinh tự đánh giá (theo chương hoặc mức độ)."""
    chu_de: str = Field(description="Tên chương/chủ đề, vd 'Chương 1', 'Đạo hàm'")
    diem: Optional[float] = Field(default=None, description="Điểm số học sinh tự đánh giá, vd 8.0")
    muc_do: Optional[str] = Field(default=None, description="Mức độ tự đánh giá dạng chữ: 'Cơ bản' | 'Khá' | 'Giỏi'")


class StudentProfileSchema(BaseModel):
    """Hồ sơ yêu cầu ra đề thi, thu thập dần qua hội thoại — mọi field đều optional vì có thể chưa được nhắc tới."""
    mon_hoc: Optional[str] = Field(default=None, description="Môn học, 1 trong: 'Toán 10' | 'Ngữ văn 10' | 'Lịch sử 10'")
    khoi_lop: Optional[int] = Field(default=None, description="Khối lớp, hiện tại luôn là 10")
    pham_vi_kiem_tra: Optional[str] = Field(default=None, description="Phạm vi chương/bài cần ra đề, vd 'Chương 1, 2, 3'")
    muc_dich: Optional[str] = Field(default=None, description="Mục đích làm đề, vd 'ôn thi cuối kì', 'kiểm tra 15 phút'")
    loai_de: Optional[str] = Field(default=None, description="Loại đề, vd 'trắc nghiệm', 'tự luận', 'kết hợp'")
    so_cau_hoi: Optional[int] = Field(default=None, description="Tổng số câu hỏi trong đề")
    thoi_gian_lam_bai: Optional[int] = Field(default=None, description="Thời gian làm bài, tính bằng phút")
    muc_tieu_diem: Optional[float] = Field(default=None, description="Điểm số mục tiêu học sinh muốn đạt, thang 10")
    ho_so_kien_thuc: Optional[List[KnowledgeItem]] = Field(default=None, description="Tự đánh giá mức độ nắm kiến thức theo từng chương")
    ghi_chu: Optional[str] = Field(default=None, description="Ghi chú thêm của học sinh, vd 'chú trọng chương 1, 3'")


class CollectInfoResponse(BaseModel):
    """Output của LLM ở bước collect_info — vừa trả lời hội thoại, vừa trích xuất field đã biết được tới thời điểm hiện tại."""
    reply: str = Field(description="Câu hỏi/phản hồi tự nhiên gửi cho học sinh, tiếng Việt")
    profile: StudentProfileSchema = Field(description="Các field đã trích xuất được từ toàn bộ hội thoại tính đến hiện tại")
    is_confirmed: bool = Field(description="True CHỈ KHI học sinh vừa xác nhận đồng ý với bản tóm tắt (câu trả lời gần nhất chứa ý đồng ý/xác nhận). False nếu đây là lần đầu tóm tắt hoặc học sinh chưa phản hồi xác nhận.")

# analysis knowledge
class KnowledgeChapterProfile(BaseModel):
    chuong: str = Field(description="Tên chương học, vd 'Chương 1: Mệnh đề và tập hợp'")
    can_nam: str = Field(description="Nội dung cần nắm ở mức cơ bản: khái niệm, hệ quả, tính chất — viết súc tích")
    can_hieu: str = Field(description="Nội dung cần hiểu sâu, bản chất, vận dụng vào dạng bài nào — viết súc tích")
    bai_hoc: List[str] = Field(description="Danh sách bài học trong chương")
    quan_he_kien_thuc: str = Field(description="Quan hệ liên kết giữa các bài học/chủ đề trong chương — viết súc tích")
    quan_he_dang_bai: str = Field(description="Quan hệ bồi đắp giữa các dạng bài tập trong chương — viết súc tích")



from typing import Literal
from pydantic import model_validator

# ── Schema cho build_matrix ──────────────────────────────────────────────────

class DoKho(BaseModel):
    de: int = Field(ge=0)
    trung_binh: int = Field(ge=0)
    kho: int = Field(ge=0)

class DangBaiItem(BaseModel):
    ten: str = Field(description="Tên dạng bài, CHỈ lấy từ hồ sơ tri thức chương, không tự tạo mới")
    so_cau: int = Field(ge=0)

class BaiHocMatrix(BaseModel):
    ten: str = Field(description="Tên bài học, lấy từ hồ sơ tri thức chương")
    so_cau: int = Field(ge=0)
    do_kho: DoKho
    dang_bai: List[DangBaiItem]

class ChapterMatrixResponse(BaseModel):
    bai_hoc: List[BaiHocMatrix]

    @model_validator(mode="after")
    def check_consistency(self):
        """Ép ràng buộc số học ngay tại schema — sai thì raise để code tự retry, không cần _validate_ch thủ công."""
        for b in self.bai_hoc:
            dk_sum = b.do_kho.de + b.do_kho.trung_binh + b.do_kho.kho
            if dk_sum != b.so_cau:
                raise ValueError(f"Bài '{b.ten}': de+trung_binh+kho={dk_sum} != so_cau={b.so_cau}")
            dang_sum = sum(d.so_cau for d in b.dang_bai)
            if dang_sum != b.so_cau:
                raise ValueError(f"Bài '{b.ten}': tổng dang_bai.so_cau={dang_sum} != so_cau={b.so_cau}")
        return self


# ── Schema cho build_specs ───────────────────────────────────────────────────

class QuestionSpec(BaseModel):
    bai: str = Field(description="Tên bài học chứa dạng bài này, lấy từ ma trận đề")
    dang_bai: str = Field(description="Tên dạng bài cụ thể, lấy đúng theo ma trận đề chương này, không tự thêm mới")
    do_kho: Literal["de", "trung_binh", "kho"]
    yeu_cau: str = Field(description="Học sinh cần làm gì cụ thể với kiến thức nào")
    muc_dich: str = Field(description="Đánh giá năng lực gì của học sinh")
    ngu_canh: List[str] = Field(description="Khái niệm/công thức/ví dụ CÓ THẬT trong tài liệu tham chiếu, không bịa")

class QuestionSpecBatch(BaseModel):
    specs: List[QuestionSpec]

# schema for generated exam
class QuestionOptions(BaseModel):
    A: str = Field(description="Nội dung đáp án A")
    B: str = Field(description="Nội dung đáp án B")
    C: str = Field(description="Nội dung đáp án C")
    D: str = Field(description="Nội dung đáp án D")


class GeneratedQuestion(BaseModel):
    id: int = Field(description="Phải khớp chính xác với id trong đặc tả (question_specs) tương ứng — không tự đặt số mới")
    type: Literal["ly_thuyet", "bai_tap"] = Field(
        description=(
            "'ly_thuyet': câu hỏi kiểm tra khái niệm, định nghĩa, tính chất — trả lời bằng ghi nhớ/suy luận logic, không cần tính toán số học. "
            "'bai_tap': câu hỏi yêu cầu thực hiện phép tính, biến đổi công thức, hoặc suy luận nhiều bước để ra một kết quả số/biểu thức cụ thể. "
            "Field này dùng để sau này định tuyến 'bai_tap' sang công cụ tính toán (SymPy) thay vì tin LLM tự tính — hiện tại LLM vẫn tự trả lời cả 2 loại."
        )
    )
    do_kho: Literal[0, 1, 2] = Field(
        description="Độ khó THỰC TẾ của câu hỏi vừa sinh: 0=dễ (nhận biết), 1=trung bình (thông hiểu/vận dụng), 2=khó (vận dụng cao)"
    )
    question: str = Field(description="Nội dung câu hỏi, đủ dữ kiện để học sinh làm bài, không mơ hồ, không thiếu thông tin")
    options: QuestionOptions = Field(description="Đúng 4 đáp án, chỉ 1 đáp án đúng, 3 đáp án nhiễu xuất phát từ lỗi sai thực tế của học sinh, không được trùng nhau")
    answer: Literal["A", "B", "C", "D"] = Field(description="Đáp án đúng duy nhất, phải khớp với options")
    giai_thich: str = Field(
        description=(
            "Giải thích CHẶT CHẼ, suy luận và tính toán từng bước chính xác nhất để chứng minh answer đúng. "
            "Câu lý thuyết: trích đúng khái niệm/định nghĩa từ tài liệu tham chiếu. "
            "Câu bài tập: trình bày đầy đủ từng bước biến đổi/tính toán, ghi rõ công thức áp dụng ở mỗi bước, không bỏ qua bước trung gian."
        )
    )
    y_tuong: str = Field(description="Mô tả ngắn gọn ý tưởng/cách ra câu hỏi, dùng để đối chiếu tránh trùng lặp ý tưởng ở các câu sau")


class GeneratedQuestionBatch(BaseModel):
    questions: List[GeneratedQuestion]

    
# ── ExamState: chạy xuyên suốt toàn bộ pipeline ─────────────────────────────

class ExamState(TypedDict):
    # Bước 1
    messages: Annotated[list, add_messages]
    student_profile: Optional[dict]          # StudentProfile.model_dump()
    profile_complete: bool                   # True khi đủ 3 trường bắt buộc

    # Bước 2
    retrieved_chunks: list[dict]
    scope_chapters: dict
    scope_lessons: dict
    retrieve_complete: bool
 

    # Bước 3
    knowledge_profile: dict
    knowledge_queue: Optional[list]    # [(chương, bài)] còn cần hỏi
    knowledge_pending: Optional[dict]  # {chương, bài, sections} đang hỏi
    knowledge_scores: dict             # {chương: {bài: {section: score}}}
    knowledge_done: bool
    completed_build_knowlege : bool
    
    # Bước 4
    exam_matrix: dict
    gop_y_matrix: str
    matrix_done: bool

    # Bước 5
    question_specs: list[dict]
    specs_done: bool
 

    # Bước 6
    generated_exam: list[dict]
    exam_memory: list[dict]
    generate_done:  bool

    # Bước 7
    exam_review: dict
    final_exam: list[dict]
    evaluate_done: bool

    # Meta
    current_step: str
    error: Optional[str]


from typing import Dict, Any

class ToolSelection(BaseModel):
    id: int = Field(description="id câu hỏi tương ứng, PHẢI khớp đúng id trong danh sách câu hỏi đã cho")
    tool_name: str = Field(description="Tên tool được chọn cho câu hỏi này — PHẢI đúng 1 trong các tool liệt kê ngay dưới câu hỏi đó, hoặc 'khong_co_tool_phu_hop' nếu không tool nào khớp")
    tool_args: Dict[str, Any] = Field(default_factory=dict, description="Tham số truyền vào tool đã chọn, đúng tên tham số theo mô tả tool, lấy giá trị từ chính dữ kiện trong câu hỏi")

class ToolSelectionBatch(BaseModel):
    selections: List[ToolSelection]