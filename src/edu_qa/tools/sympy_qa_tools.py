import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..","..")))

from langchain_core.tools import tool
import sympy as sp


def _to_expr(expression: str):
    x, y = sp.symbols("x y")
    return sp.sympify(expression, locals={"x": x, "y": y})


@tool
def sympy_diff(expression: str, variable: str = "x") -> str:
    """Tính đạo hàm của một biểu thức toán học theo một biến số.

    Dùng khi câu hỏi yêu cầu tính đạo hàm (derivative), y', f'(x).

    Args:
        expression: biểu thức viết theo cú pháp SymPy, ví dụ "x**3 + 2*x**2 - 5*x"
            hoặc "(2*x+1)**3". Lũy thừa dùng "**", phép nhân phải viết
            tường minh bằng "*".
        variable: biến số cần lấy đạo hàm theo, mặc định "x".

    Returns:
        Kết quả đạo hàm dạng chuỗi, hoặc chuỗi bắt đầu bằng "LOI:" nếu
        biểu thức không hợp lệ.
    """
    try:
        var = sp.symbols(variable)
        expr = _to_expr(expression)
        result = sp.diff(expr, var)
        return str(sp.simplify(result))
    except Exception as e:
        return f"LOI: khong the tinh dao ham - {e}"


@tool
def sympy_solve(expression: str, variable: str = "x") -> str:
    """Giải phương trình để tìm nghiệm theo một biến số.

    Dùng khi câu hỏi yêu cầu tìm x, giải phương trình, tìm nghiệm.

    Args:
        expression: biểu thức vế trái khi phương trình = 0, ví dụ
            "x**2 - 5*x + 6" (tương ứng phương trình x^2 - 5x + 6 = 0).
        variable: biến số cần giải, mặc định "x".

    Returns:
        Danh sách nghiệm dạng chuỗi, hoặc chuỗi bắt đầu bằng "LOI:" nếu
        không giải được.
    """
    try:
        var = sp.symbols(variable)
        expr = _to_expr(expression)
        result = sp.solve(expr, var)
        return str([str(r) for r in result])
    except Exception as e:
        return f"LOI: khong the giai - {e}"


@tool
def sympy_simplify(expression: str) -> str:
    """Rút gọn một biểu thức toán học về dạng đơn giản nhất.

    Dùng khi câu hỏi yêu cầu rút gọn, biến đổi biểu thức về dạng gọn hơn.

    Args:
        expression: biểu thức cần rút gọn, viết theo cú pháp SymPy.

    Returns:
        Biểu thức đã rút gọn dạng chuỗi, hoặc chuỗi bắt đầu bằng "LOI:"
        nếu không xử lý được.
    """
    try:
        expr = _to_expr(expression)
        result = sp.simplify(expr)
        return str(result)
    except Exception as e:
        return f"LOI: khong the rut gon - {e}"


@tool
def sympy_evaluate(expression: str) -> str:
    """Tính giá trị số cụ thể của một biểu thức toán học.

    Dùng khi câu hỏi yêu cầu ra một con số cụ thể (không phải rút gọn
    hay đạo hàm), ví dụ tính giá trị biểu thức tại một điểm cho trước.

    Args:
        expression: biểu thức cần tính, viết theo cú pháp SymPy. Nếu cần
            thay giá trị cụ thể vào biến, hãy thay trực tiếp trong
            expression trước khi gọi (ví dụ thay x=2 thành "2**3 + 1").

    Returns:
        Giá trị số dạng chuỗi, hoặc chuỗi bắt đầu bằng "LOI:" nếu không
        tính được.
    """
    try:
        expr = _to_expr(expression)
        result = sp.N(expr)
        return str(result)
    except Exception as e:
        return f"LOI: khong the tinh gia tri - {e}"


from src.edu_qa.tools.set_tools import SET_TOOLS
from src.edu_qa.tools.inequality_tools import INEQUALITY_TOOLS
from src.edu_qa.tools.quadratic_tools import QUADRATIC_TOOLS

QA_TOOLS = [sympy_diff, sympy_solve, sympy_simplify, sympy_evaluate] + SET_TOOLS + INEQUALITY_TOOLS + QUADRATIC_TOOLS
# print("QA_TOOLS =", [t.name for t in QA_TOOLS])