from typing import Literal
from langchain_core.tools import tool


@tool
def approve_roadmap() -> str:
    """Học sinh đồng ý, hài lòng với sườn lộ trình, không cần sửa gì thêm.

    Ví dụ: "ok", "được rồi", "chốt", "đồng ý".
    """
    return "approved"


@tool
def revise_roadmap(yeu_cau: str) -> str:
    """Học sinh muốn đổi sườn lộ trình trong khi thông tin cá nhân của họ vẫn đúng.

    Ví dụ: đổi thứ tự chương, thêm/bớt chương, tăng/giảm trọng tâm một phần.

    Args:
        yeu_cau: yêu cầu chỉnh sửa, viết rõ và đủ ý.
    """
    return "revise"


@tool
def request_profile_update(
    fields: list[Literal["muc_tieu", "lich_hoc", "nang_luc", "so_thich_hoc", "ca_nhan"]],
    ly_do: str,
) -> str:
    """Học sinh nói thông tin về bản thân đã đổi hoặc ghi sai, nên cần thu thập lại trước khi sửa sườn.

    Ví dụ: "mình bận tối thứ 7", "mục tiêu của mình là 9 điểm", "mình yếu chương III hơn bạn ghi".

    Args:
        fields: nhóm thông tin cần cập nhật.
        ly_do: học sinh nói gì dẫn đến việc cập nhật.
    """
    return "update_profile"


@tool
def reply_to_student(noi_dung: str) -> str:
    """Trả lời học sinh mà không đổi gì: giải thích vì sao sườn xếp như vậy, hoặc hỏi lại 1 câu khi góp ý còn mơ hồ.

    Args:
        noi_dung: nội dung trả lời, chỉ dựa trên hồ sơ và sườn hiện tại.
    """
    return "reply"


FEEDBACK_TOOLS = [approve_roadmap, revise_roadmap, request_profile_update, reply_to_student]