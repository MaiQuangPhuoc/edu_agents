from langchain_core.tools import tool
import sympy as sp

x = sp.symbols("x")


def _to_expr(a, b, c):
    return sp.sympify(a) * x**2 + sp.sympify(b) * x + sp.sympify(c)


@tool
def quadratic_vertex(a: float, b: float, c: float) -> str:
    """Tìm tọa độ đỉnh và trục đối xứng của hàm số bậc hai y = ax^2 + bx + c.

    Dùng khi câu hỏi yêu cầu tìm đỉnh, trục đối xứng, hoặc giá trị lớn nhất/nhỏ nhất
    của hàm số bậc hai.

    Args:
        a: hệ số bậc 2 (a khác 0).
        b: hệ số bậc 1.
        c: hằng số.

    Returns:
        Chuỗi mô tả tọa độ đỉnh, trục đối xứng, và hàm đồng biến/nghịch biến trên
        khoảng nào, hoặc "LOI:" nếu lỗi.
    """
    try:
        a_v, b_v, c_v = sp.sympify(a), sp.sympify(b), sp.sympify(c)
        if a_v == 0:
            return "LOI: a phai khac 0 de la ham so bac hai"

        x_dinh = -b_v / (2 * a_v)
        y_dinh = c_v - b_v**2 / (4 * a_v)
        huong = "bề lõm hướng lên (a>0), đỉnh là điểm cực tiểu" if a_v > 0 else "bề lõm hướng xuống (a<0), đỉnh là điểm cực đại"

        return (
            f"Đỉnh I({x_dinh}, {y_dinh}). Trục đối xứng: x = {x_dinh}. "
            f"Đồ thị có {huong}."
        )
    except Exception as e:
        return f"LOI: khong the tim dinh - {e}"


@tool
def quadratic_sign(a: float, b: float, c: float) -> str:
    """Xét dấu của tam thức bậc hai f(x) = ax^2 + bx + c trên các khoảng.

    Dùng khi câu hỏi yêu cầu xét dấu tam thức bậc hai, hoặc giải bất phương trình
    bậc hai dạng ax^2 + bx + c > 0 (hoặc <0, >=0, <=0).

    Args:
        a: hệ số bậc 2 (a khác 0).
        b: hệ số bậc 1.
        c: hằng số.

    Returns:
        Chuỗi mô tả nghiệm (nếu có) và dấu của f(x) trên từng khoảng, hoặc "LOI:" nếu lỗi.
    """
    try:
        expr = _to_expr(a, b, c)
        a_v = sp.sympify(a)
        roots = sp.solve(sp.Eq(expr, 0), x)

        if not roots:
            dau = "luôn dương (a>0)" if a_v > 0 else "luôn âm (a<0)"
            return f"Phương trình vô nghiệm (delta < 0). f(x) {dau} với mọi x."

        if len(roots) == 1:
            r = roots[0]
            dau = "dương" if a_v > 0 else "âm"
            return f"Phương trình có nghiệm kép x = {r}. f(x) {dau} với mọi x khác {r}, f({r}) = 0."

        r1, r2 = sorted(roots, key=lambda r: float(r))
        if a_v > 0:
            return (
                f"Hai nghiệm x1={r1}, x2={r2}. f(x) > 0 khi x < {r1} hoặc x > {r2}; "
                f"f(x) < 0 khi {r1} < x < {r2}."
            )
        else:
            return (
                f"Hai nghiệm x1={r1}, x2={r2}. f(x) < 0 khi x < {r1} hoặc x > {r2}; "
                f"f(x) > 0 khi {r1} < x < {r2}."
            )
    except Exception as e:
        return f"LOI: khong the xet dau - {e}"


QUADRATIC_TOOLS = [quadratic_vertex, quadratic_sign]