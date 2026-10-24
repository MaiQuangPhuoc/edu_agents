from typing import Literal, Optional, TypedDict, Annotated
from datetime import datetime
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

# ───────── 1. STUDENT MODEL ─────────

class ThongTinCaNhan(BaseModel):
    ho_ten: str = ""
    khoi_lop: int = 10
    so_thich: list[str] = []
    hoat_dong_ngoai_khoa: list[str] = []      # tác động từ ngoài vào lộ trình

class NangLucChuDe(BaseModel):
    chapter_id: str
    lesson: str = ""
    muc_nam: Optional[float] = None           # 0-1, None = chưa đánh giá
    do_tin_cay: float = 0.0                   # dữ liệu càng nhiều càng cao
    nguon: Literal["tu_danh_gia", "bai_kiem_tra", "chat"] = "tu_danh_gia"
    cap_nhat: Optional[datetime] = None

class NangLucMonHoc(BaseModel):
    mon_hoc: str
    diem_hien_tai: Optional[float] = None
    diem_manh: list[str] = []
    diem_yeu: list[str] = []
    da_test_dau_vao: bool = Field(False, description="True sau khi học sinh làm bài test đầu vào và hệ thống chấm xong")
    chu_de: list[NangLucChuDe] = []

class MucTieu(BaseModel):
    mon_hoc: str
    muc_tieu_diem: Optional[float] = None
    han_chot: Optional[str] = None            # ví dụ "thi học kì 2"
    ngay_ket_thuc: Optional[str] = Field(None, description="Ngày cụ thể, định dạng YYYY-MM-DD")
    so_tuan_con_lai: Optional[int] = Field(None, description="Còn khoảng mấy tuần; dùng khi học sinh không nêu ngày")
    # uu_tien: Literal["diem_so", "hieu_ban_chat", "ca_hai"] = "ca_hai"
    uu_tien: Optional[Literal["diem_so", "hieu_ban_chat", "ca_hai"]] = None
    dang_bai_can_giu: list[str] = []          # dạng toán muốn tập trung

class SoThichHoc(BaseModel):
    dung_tai_lieu: Optional[bool] = None
    dung_video: Optional[bool] = None
    bai_tap_sau_buoi: Optional[bool] = None
    tom_tat_cuoi_buoi: Optional[bool] = None
    thoi_luong_buoi_phut: Optional[int] = None

class LichHoc(BaseModel):
    so_buoi_tuan: Optional[int] = None
    khung_gio_ranh: dict[str, list[str]] = {}  # {"thu_2": ["19:00-21:00"]}
    lich_ban: list[str] = []                   # học thêm, hoạt động cố định

class TienDo(BaseModel):                       # Progress Agent ghi, các agent khác chỉ đọc
    ti_le_hoan_thanh: Optional[float] = None
    so_ngay_lien_tiep: int = 0
    lan_hoat_dong_cuoi: Optional[datetime] = None
    tin_hieu_dong_luc: Optional[str] = None    # chưa chốt cách đo

class StudentModel(BaseModel):
    student_id: str = ""   # code gán sau, LLM không cần điền
    ca_nhan: ThongTinCaNhan = ThongTinCaNhan()
    nang_luc: list[NangLucMonHoc] = []
    muc_tieu: list[MucTieu] = []
    so_thich_hoc: SoThichHoc = SoThichHoc()
    lich_hoc: LichHoc = LichHoc()
    tien_do: TienDo = TienDo()
    version: int = 1
    updated_at: Optional[datetime] = None

class CollectTurn(BaseModel):
    student_model: StudentModel
    tin_nhan: str
    hoan_tat: bool = False

class GuardResult(BaseModel):
    hop_le: bool
    tra_loi: str = ""

class ProfilePatch(BaseModel):
    muc_tieu: Optional[list[MucTieu]] = None
    lich_hoc: Optional[LichHoc] = None
    nang_luc: Optional[list[NangLucMonHoc]] = None
    so_thich_hoc: Optional[SoThichHoc] = None
    ca_nhan: Optional[ThongTinCaNhan] = None

class CollectPatchTurn(BaseModel):
    patch: ProfilePatch
    tin_nhan: str
    hoan_tat: bool = False

class SearchQuery(BaseModel):
    query: str
    subject: str
    chapter_id: Optional[str] = None
    nguon: Literal["sgk", "web", "video"] = "sgk"

class QueryPlan(BaseModel):
    queries: list[SearchQuery]

class TaiNguyenGoiY(BaseModel):
    loai: Literal["tai_lieu", "video", "giao_trinh"]
    tieu_de: str
    url: Optional[str] = None
    ghi_chu: str = Field("", description="Một câu: tài nguyên này giúp gì cho giai đoạn")

class ChuongKeHoach(BaseModel):
    chapter_id: str = Field(description="PHẢI lấy từ cấu trúc chương trình đã cho")
    lessons: list[str] = Field(description="Tên bài, PHẢI lấy từ cấu trúc chương trình")
    ly_do: str = Field(description="Vì sao xếp chương này vào giai đoạn này (dựa trên hồ sơ/tài liệu)")

class GiaiDoan(BaseModel):
    thu_tu: int
    ten: str
    mon_hoc: str
    muc_tieu: str
    chapters: list[ChuongKeHoach]
    tieu_chi_hoan_thanh: str
    tai_nguyen: list[TaiNguyenGoiY] = Field(default=[], description="Tối đa 3 gợi ý, chỉ lấy từ kết quả tra cứu")

class MasterRoadmap(BaseModel):
    muc_tieu_tong: str
    chien_luoc: str = Field(description="Chiến lược ngắn gọn để đạt mục tiêu")
    giai_doan: list[GiaiDoan]
    gia_dinh: list[str] = Field(default=[], description="Các điểm là đề xuất/giả định vì chưa có tài liệu xác nhận")

class BatchPlan(BaseModel):
    giai_doan: list[GiaiDoan]
    tom_tat: list[str] = Field(description="Mỗi chương trong phạm vi một dòng ý chính ngắn")
    gia_dinh: list[str] = Field(default=[], description="Điểm là đề xuất/giả định vì chưa có tài liệu xác nhận")

class Overview(BaseModel):
    muc_tieu_tong: str
    chien_luoc: str = Field(description="Chiến lược ngắn gọn để đạt mục tiêu")

class ToolCallPlan(BaseModel):
    tool: Literal["search_web_documents", "search_videos"]
    query: str
    chapter_id: Optional[str] = None

class ToolPlan(BaseModel):
    calls: list[ToolCallPlan]

# ───────── 2. TIN NHẮN A2A ─────────

# class AgentMessage(BaseModel):
#     sender: Literal["student_model", "planning", "roadmap", "progress", "report", "exam"]
#     receiver: str
#     type: Literal["request", "result", "replan", "reassess"]
#     payload: dict = {}
#     created_at: datetime = Field(default_factory=datetime.now)

class HandoffMessage(BaseModel):
    sender: Literal["collect", "planning", "roadmap", "progress", "report", "exam"]
    receiver: Literal["collect", "planning", "roadmap", "progress", "report", "exam"]
    type: Literal["request", "result", "update_profile", "profile_updated", "revise_roadmap"]
    payload: dict = {}
    created_at: datetime = Field(default_factory=datetime.now)



# ───────── LEARNING PATH ─────────

Difficulty = Literal["easy", "medium", "hard"]


class Task(BaseModel):
    id: str
    goal: str                       # mục tiêu của bước, ví dụ "Chuẩn bị tài nguyên cho chương I"
    depends_on: list[str] = []
    origin: Literal["fixed", "generated"] = "generated"


class TaskPlan(BaseModel):
    tasks: list[Task]


class Resource(BaseModel):
    type: Literal["document", "video", "curriculum"]
    title: str
    url: Optional[str] = None
    note: str = ""


class LinkedLesson(BaseModel):
    chapter_id: str
    lesson: str
    relation: str

class LessonKnowledge(BaseModel):
    lesson: str
    key_points: list[str] = []
    must_know: list[str] = []
    must_understand: list[str] = []
    problem_types: list[str] = []
    related: list[LinkedLesson] = []


class ChapterKnowledge(BaseModel):
    chapter_id: str = ""
    lessons: list[LessonKnowledge]

class Activity(BaseModel):
    type: Literal["lecture", "reading", "video", "exercise", "summary", "review"]
    content: str
    minutes: int
    difficulty: Difficulty = "easy"
    problem_type: str = ""


class Assessment(BaseModel):
    chapter_ids: list[str]
    num_questions: int


class Session(BaseModel):
    date: str                                   # YYYY-MM-DD
    start_time: str                             # HH:MM
    minutes: int
    type: Literal["lesson", "review", "assessment"] = "lesson"
    chapter_id: str
    lesson: str
    key_points: list[str] = []
    must_know: list[str] = []
    must_understand: list[str] = []
    related: list[LinkedLesson] = []
    difficulty: Difficulty = "easy"
    activities: list[Activity] = []
    resources: list[Resource] = []
    assessment: Optional[Assessment] = None     # only for type == "assessment"


class Week(BaseModel):
    week_no: int
    start_date: str
    end_date: str
    goal: str
    sessions: list[Session] = []                # empty = outline-only week

class LessonRef(BaseModel):
    chapter_id: str
    lesson: str


class BriefWeek(BaseModel):
    """Mức vừa: dùng cho mọi tuần của mọi giai đoạn (LLM sinh)."""
    week_no: int                                # đánh số liên tục qua các giai đoạn
    goal: str
    lessons: list[LessonRef]
    activity_types: list[str] = []
    difficulty_trend: str = ""                  # ví dụ "dễ → vừa"
    total_hours: float = 0
    has_assessment: bool = False                # tuần có buổi kiểm tra định kỳ


class PhaseOutline(BaseModel):
    phase: int
    weeks: list[BriefWeek]


class OutlineWeek(BaseModel):            # LLM sinh, phẳng
    phase: int
    goal: str
    lessons: list[str]                   # mã bài, ví dụ "I.1"
    activity_types: list[str] = []
    difficulty_trend: str = ""
    has_assessment: bool = False

class OutlinePlan(BaseModel):
    weeks: list[OutlineWeek]

class ActivityDraft(BaseModel):
    type: Literal["lecture", "reading", "video", "exercise", "summary", "review"]
    content: str
    minutes: int

class SessionDraft(BaseModel):
    lesson: str                          # mã bài
    type: Literal["lesson", "review", "assessment"] = "lesson"
    activities: list[ActivityDraft]
    resources: list[Resource] = []

class WeekDraft(BaseModel):
    goal: str
    sessions: list[SessionDraft]

class ReviewIssue(BaseModel):
    week_no: int = 0
    problem: str

class ReviewResult(BaseModel):           # rỗng = ổn
    issues: list[ReviewIssue] = []





class Schedule(BaseModel):
    start_date: str
    end_date: Optional[str] = None
    total_weeks: int
    sessions_per_week: int
    minutes_per_session: int

class LearningPath(BaseModel):
    current_phase: int
    schedule: Schedule
    outline: list[PhaseOutline] = []     # THÊM: tuần mức vừa của mọi giai đoạn
    weeks: list[Week]                    # giữ nguyên: tuần chi tiết của giai đoạn hiện tại
    assumptions: list[str] = []



# ───────── 3. STATE CHUNG ─────────

class PlanState(TypedDict, total=False):
    # chung
    messages: Annotated[list, add_messages]      # hội thoại với học sinh
    student_id: str
    guard_ok: bool
    current_step: str

    # collect
    student_model: dict
    student_model_prev: dict
    search_queries: list[dict]
    model_done: bool
    update_request: dict                         # Planning -> collect: {"fields": [...], "ly_do": "..."}

    # planning (sườn lộ trình)
    plan_messages: list    
    plan_draft: dict                             # {giai_doan, gia_dinh, tom_tat} ghép từ các lô
    plan_transcript: str 
                          # vòng ReAct của planner, ghi đè mỗi lần chạy lại
    master_roadmap: dict
    roadmap_prev: dict
    master_done: bool
    roadmap_status: str                          # draft | awaiting_feedback | revising | updating_profile
                                                 # | profile_changed | approved | path_ready
    feedback: str
    revision_count: int
    decision: str
    decision_args: dict
    inbox: list[dict]         
    
    entry_test: dict                             # {subject, key_file, result}; roadmap_status thêm: awaiting_test_answers | entry_test_failed
    entry_done: bool                             # đã chấm xong bài test đầu vào                   # nhật ký chuyển giao (HandoffMessage)

    # learning path (kế hoạch chi tiết)
    vi_tri_hien_tai: int
    lp_window: dict
    lp_tasks: list[dict]
    lp_results: dict

    lp_outline: list[dict]        # kết quả outline của mọi giai đoạn (PhaseOutline.model_dump())

    lp_codes: dict                # mã bài -> {phase, chapter_id, lesson}
    lp_knowledge: dict            # {chapter_id: ChapterKnowledge dict}, nạp từ cache một lần


    lp_replan_count: int
    lp_draft: dict
    lp_issues: dict                              # {"week_no": [lỗi]}
    lp_revision_count: int
    lp_reviewed: bool                            # LLM review chỉ chạy một lần

    learning_path: dict
    lp_file: str                                 # đường dẫn file JSON lộ trình (UI mở bằng nút)