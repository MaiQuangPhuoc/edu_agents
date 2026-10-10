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
    chu_de: list[NangLucChuDe] = []

class MucTieu(BaseModel):
    mon_hoc: str
    muc_tieu_diem: Optional[float] = None
    han_chot: Optional[str] = None            # ví dụ "thi học kì 2"
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
    student_id: str
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

class MasterRoadmap(BaseModel):
    muc_tieu_tong: str
    chien_luoc: str = Field(description="Chiến lược ngắn gọn để đạt mục tiêu")
    giai_doan: list[GiaiDoan]
    gia_dinh: list[str] = Field(default=[], description="Các điểm là đề xuất/giả định vì chưa có tài liệu xác nhận")
# ───────── 2. TIN NHẮN A2A ─────────

class AgentMessage(BaseModel):
    sender: Literal["student_model", "planning", "roadmap", "progress", "report", "exam"]
    receiver: str
    type: Literal["request", "result", "replan", "reassess"]
    payload: dict = {}
    created_at: datetime = Field(default_factory=datetime.now)

# ───────── 3. STATE CHUNG ─────────

class PlanState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    plan_messages: Annotated[list, add_messages]   # vòng ReAct của Planning Agent
    student_id: str
    student_model: dict           # StudentModel.model_dump()
    master_roadmap: dict          # Planning Agent ghi
    weekly_plan: dict             # Roadmap Agent ghi
    a2a_inbox: list[dict]         # AgentMessage.model_dump(), tin chờ xử lý
    replan_reason: str
    model_done: bool              # cờ *_done giống ExamState
    master_done: bool
    weekly_done: bool
    current_step: str