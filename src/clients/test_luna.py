import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import datetime
from langchain_core.tools import tool
from pydantic import BaseModel
from src.configs import env_config
from src.clients.llm import LLMClient
from src.clients.api_logger import LOG_DIR, print_usage_summary
from src.state_plan import BatchPlan


class Mini(BaseModel):
    ten_chuong: str
    so_buoi: int


@tool
def ping(x: int) -> str:
    """Trả về số x kèm chữ ok."""
    return f"{x} ok"


def step(name, fn):
    print(f"\n=== {name} ===")
    try:
        fn()
    except Exception as e:
        print("LỖI:", type(e).__name__, str(e)[:300])


def last_rows(n):
    path = LOG_DIR / f"{datetime.now():%Y-%m-%d}.md"
    rows = [l for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("| 20")] if path.exists() else []
    print("\n".join(rows[-n:]))


client = LLMClient(model=env_config.plan_model, api_provider=env_config.plan_provider)
print("Client:", env_config.plan_provider, env_config.plan_model, type(client._llm).__name__)


def t_mini():
    res = client.invoke_structured(Mini, [{"role": "user", "content": "Chương I Toán 10 là Mệnh đề và tập hợp, học 6 buổi."}],
                                   max_tokens=2000)
    print("Kết quả:", res)


DATA = """Học sinh lớp 10, Toán 10: điểm hiện tại 6.5, mục tiêu 8 điểm, còn 6 tuần, 3 buổi mỗi tuần, mỗi buổi 45 phút.
Chương I (Mệnh đề và tập hợp): mức Yếu (muc_nam 0.30). Chương II (Bất phương trình và hệ bất phương trình bậc nhất hai ẩn): mức Trung bình (0.55).
Giáo án tham khảo: chương I gồm 3 bài và bài tập cuối chương, khoảng 6 buổi; chương II khoảng 5 buổi."""


def t_batch():
    msgs = [{"role": "system", "content": "Bạn là giáo viên lập sườn lộ trình học. Chỉ dựa vào dữ liệu được cung cấp, không bịa."},
            {"role": "user", "content": DATA + "\nPHẠM VI: Toán 10, chương I, II. Sinh giai_doan, tom_tat (mỗi chương một dòng), gia_dinh."}]
    res = client.invoke_structured(BatchPlan, msgs, max_tokens=6000)
    if res is None:
        print("invoke_structured trả None (thất bại)")
        return
    print("Số giai đoạn:", len(res.giai_doan))
    print("Tóm tắt:", res.tom_tat)
    print("Giả định:", res.gia_dinh)


def t_tools():
    r = client._llm.bind_tools([ping]).invoke("Hãy gọi công cụ ping với x=3.")
    print("tool_calls:", r.tool_calls)


STATIC = "\n".join(f"{i}. Chỉ dựa vào thông tin được cung cấp, không bịa chương, bài hay số liệu; điều chưa chắc chắn phải ghi rõ là giả định."
                   for i in range(1, 61))


def t_cache():
    for q in ("Chương II Toán 10 học mấy buổi?", "Chương III Toán 10 học mấy buổi?"):
        res = client.invoke_structured(Mini, [{"role": "system", "content": STATIC},
                                              {"role": "user", "content": q}], max_tokens=2000)
        print(q, "->", res)
    print("Hai dòng log gần nhất (cột Cached của lần 2 > 0 nghĩa là trúng cache):")
    last_rows(2)


# step("1. structured schema nhỏ", t_mini)
# step("2. structured BatchPlan (schema thật)", t_batch)
# step("3. gọi tool trực tiếp (bind_tools)", t_tools)
# step("4. thử prompt cache (2 lần cùng system dài)", t_cache)
# print()
# print_usage_summary()
# print("\nCác dòng log gần nhất:")
# last_rows(6)