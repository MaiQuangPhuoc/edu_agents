import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from typing import Literal
from langchain_core.tools import tool
import sympy as sp

x = sp.symbols("x")


# ── Nhóm Đại số / Giải tích ──────────────────────────────────────────────────

@tool
def algebra_tool(operation: Literal["diff", "solve", "simplify", "evaluate"], expression: str, variable: str = "x") -> str:
    """Tool đại số/giải tích: đạo hàm, giải phương trình, rút gọn, tính giá trị số.

    operation="diff": tính đạo hàm của expression theo variable.
    operation="solve": giải phương trình expression=0 theo variable.
    operation="simplify": rút gọn expression.
    operation="evaluate": tính giá trị số của expression (đã thay sẵn số vào biến).

    Args:
        operation: loại phép toán cần thực hiện.
        expression: biểu thức SymPy, ví dụ "x**2 - 4*x + 3".
        variable: biến số, mặc định "x".
    """
    try:
        var = sp.symbols(variable)
        expr = sp.sympify(expression)

        if operation == "diff":
            return str(sp.diff(expr, var))
        if operation == "solve":
            return str(sp.solve(sp.Eq(expr, 0), var))
        if operation == "simplify":
            return str(sp.simplify(expr))
        if operation == "evaluate":
            return str(expr.evalf())
        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


# ── Nhóm Tập hợp ──────────────────────────────────────────────────────────

def _parse_set(items: str) -> set:
    return {sp.sympify(i.strip()) for i in items.split(",") if i.strip()}


@tool
def set_tool(operation: Literal["union", "intersection", "difference", "subset"], set_a: str, set_b: str) -> str:
    """Tool tập hợp: hợp, giao, hiệu, kiểm tra tập con giữa hai tập hợp số.

    operation="union": tính A ∪ B.
    operation="intersection": tính A ∩ B.
    operation="difference": tính A \\ B.
    operation="subset": kiểm tra A có phải tập con của B không.

    Args:
        operation: loại phép toán tập hợp cần thực hiện.
        set_a: các phần tử tập A, cách nhau bởi dấu phẩy, ví dụ "1, 2, 3".
        set_b: các phần tử tập B, cách nhau bởi dấu phẩy.
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)

        if operation == "union":
            result = sorted(a | b, key=lambda v: float(v))
            return "{" + ", ".join(str(v) for v in result) + "}"
        if operation == "intersection":
            result = sorted(a & b, key=lambda v: float(v))
            return "{" + ", ".join(str(v) for v in result) + "}"
        if operation == "difference":
            result = sorted(a - b, key=lambda v: float(v))
            return "{" + ", ".join(str(v) for v in result) + "}"
        if operation == "subset":
            return str(a.issubset(b))
        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


# ── Nhóm Bất phương trình bậc nhất hai ẩn ──────────────────────────────────

@tool
def linear_inequality_tool(
    operation: Literal["check_point", "optimize"],
    a: float,
    b: float,
    c: float = 0,
    x0: float = 0,
    y0: float = 0,
    sign: str = "<=",
    vertices: str = "",
    mode: str = "max",
) -> str:
    """Tool bất phương trình bậc nhất hai ẩn: kiểm tra điểm, tìm GTLN/GTNN trên miền đa giác.

    operation="check_point": kiểm tra điểm (x0, y0) có thỏa ax+by (sign) c không.
    operation="optimize": tìm GTLN/GTNN của F=ax+by trên miền đa giác (vertices).

    Args:
        operation: loại phép toán cần thực hiện.
        a: hệ số của x.
        b: hệ số của y.
        c: hằng số vế phải (dùng cho check_point).
        x0: hoành độ điểm cần kiểm tra (dùng cho check_point).
        y0: tung độ điểm cần kiểm tra (dùng cho check_point).
        sign: dấu bất phương trình "<=", ">=", "<", ">" (dùng cho check_point).
        vertices: tọa độ đỉnh đa giác dạng "x1,y1; x2,y2; x3,y3" (dùng cho optimize).
        mode: "max" hoặc "min" (dùng cho optimize).
    """
    try:
        if operation == "check_point":
            value = a * x0 + b * y0
            ops = {"<=": value <= c, ">=": value >= c, "<": value < c, ">": value > c}
            if sign not in ops:
                return f"LOI: dau khong hop le - {sign}"
            return str(ops[sign])

        if operation == "optimize":
            points = []
            for pair in vertices.split(";"):
                xs, ys = pair.strip().split(",")
                points.append((sp.sympify(xs.strip()), sp.sympify(ys.strip())))
            values = [(a * px + b * py, (px, py)) for px, py in points]
            best = max(values, key=lambda v: float(v[0])) if mode == "max" else min(values, key=lambda v: float(v[0]))
            return f"F = {best[0]} tai diem ({best[1][0]}, {best[1][1]})"

        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


# ── Nhóm Hàm số bậc hai ──────────────────────────────────────────────────

@tool
def quadratic_tool(operation: Literal["vertex", "sign"], a: float, b: float, c: float) -> str:
    """Tool hàm số bậc hai: tìm đỉnh/trục đối xứng, hoặc xét dấu tam thức.

    operation="vertex": tìm tọa độ đỉnh, trục đối xứng của y=ax^2+bx+c.
    operation="sign": xét dấu tam thức f(x)=ax^2+bx+c trên các khoảng.

    Args:
        operation: loại phép toán cần thực hiện.
        a: hệ số bậc 2 (khác 0).
        b: hệ số bậc 1.
        c: hằng số.
    """
    try:
        a_v, b_v, c_v = sp.sympify(a), sp.sympify(b), sp.sympify(c)
        if a_v == 0:
            return "LOI: a phai khac 0"

        if operation == "vertex":
            x_dinh = -b_v / (2 * a_v)
            y_dinh = c_v - b_v**2 / (4 * a_v)
            huong = "bề lõm hướng lên (a>0), đỉnh là điểm cực tiểu" if a_v > 0 else "bề lõm hướng xuống (a<0), đỉnh là điểm cực đại"
            return f"Đỉnh I({x_dinh}, {y_dinh}). Trục đối xứng: x = {x_dinh}. Đồ thị có {huong}."

        if operation == "sign":
            expr = a_v * x**2 + b_v * x + c_v
            roots = sp.solve(sp.Eq(expr, 0), x)
            if not roots:
                dau = "luôn dương (a>0)" if a_v > 0 else "luôn âm (a<0)"
                return f"Vô nghiệm (delta<0). f(x) {dau} với mọi x."
            if len(roots) == 1:
                r = roots[0]
                dau = "dương" if a_v > 0 else "âm"
                return f"Nghiệm kép x={r}. f(x) {dau} với mọi x khác {r}, f({r})=0."
            r1, r2 = sorted(roots, key=lambda r: float(r))
            if a_v > 0:
                return f"Hai nghiệm x1={r1}, x2={r2}. f(x)>0 khi x<{r1} hoặc x>{r2}; f(x)<0 khi {r1}<x<{r2}."
            return f"Hai nghiệm x1={r1}, x2={r2}. f(x)<0 khi x<{r1} hoặc x>{r2}; f(x)>0 khi {r1}<x<{r2}."

        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


MATH_TOOLS = [algebra_tool, set_tool, linear_inequality_tool, quadratic_tool]