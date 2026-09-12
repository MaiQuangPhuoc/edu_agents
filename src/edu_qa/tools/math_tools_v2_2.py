import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from typing import Literal, Optional
from langchain_core.tools import tool
import sympy as sp
from sympy.calculus.util import continuous_domain

x, y = sp.symbols("x y")


# ─────────────────────────────────────────────────────────────────────────
# Helper functions (không phải tool, chỉ hỗ trợ parse dữ liệu đầu vào)
# ─────────────────────────────────────────────────────────────────────────

def _parse_set(items: str) -> set:
    return {sp.sympify(i.strip()) for i in items.split(",") if i.strip()}


def _parse_numbers(items: str) -> list:
    return [sp.sympify(i.strip()) for i in items.split(",") if i.strip()]


def _parse_vector(v: str) -> tuple:
    parts = v.split(",")
    if len(parts) != 2:
        raise ValueError(f"Vecto phai co dung 2 thanh phan (x,y), nhan duoc: {v}")
    return sp.sympify(parts[0].strip()), sp.sympify(parts[1].strip())


def _deg(val) -> sp.Expr:
    """Chuyển góc độ (nsimplify để giữ dạng phân số đẹp) sang radian."""
    return sp.rad(sp.nsimplify(val))


def _to_deg(rad_val) -> sp.Expr:
    return sp.deg(rad_val)


# ═══════════════════════════════════════════════════════════════════════
# CHƯƠNG I — Mệnh đề và tập hợp (c_1)
# ═══════════════════════════════════════════════════════════════════════

@tool
def xet_menh_de_tool(bieu_thuc: str) -> str:
    """Xác định một mệnh đề (câu khẳng định) là đúng hay sai.

    Dùng khi:
    - Xét tính đúng sai của một mệnh đề.
    - Kiểm tra một khẳng định toán học có đúng không.
    - Đánh giá các mệnh đề về chia hết, chẵn lẻ hoặc so sánh số.

    Ví dụ:
    - "15 chia hết cho 3 đúng hay sai?"
    - "Số 7 là số chẵn đúng hay sai?"
    - "Mệnh đề sau đúng hay sai?"

    Args:
        bieu_thuc: biểu thức logic hoặc so sánh dạng SymPy/Python,
            ví dụ "15 % 3 == 0", "Eq(2+2,4)", "sqrt(4)==2".
    """
    try:
        expr = sp.sympify(bieu_thuc)
        result = bool(expr)
        return "Đúng" if result else "Sai"
    except Exception as e:
        return f"LOI: {e}"

@tool
def phu_dinh_menh_de_tool(bieu_thuc: str) -> str:
    """Viết mệnh đề phủ định của một mệnh đề cho trước.

    Dùng khi:
    - Viết mệnh đề phủ định của P.
    - Tìm phủ định của một khẳng định.
    - Xử lý các mệnh đề chứa điều kiện hoặc quan hệ so sánh.

    Ví dụ:
    - "Phủ định của x > 3 là gì?"
    - "Viết mệnh đề phủ định của n chia hết cho 5."
    - "Lập mệnh đề phủ định của P."

    Args:
        bieu_thuc: biểu thức so sánh dạng SymPy,
            ví dụ "x > 3", "Eq(x,5)".
    """
    try:
        expr = sp.sympify(bieu_thuc)
        neg = sp.Not(expr) if not isinstance(expr, sp.core.relational.Relational) else ~expr
        return str(neg)
    except Exception as e:
        return f"LOI: {e}"

@tool
def hop_tap_hop_tool(set_a: str, set_b: str) -> str:
    """Tính hợp của hai tập hợp (A ∪ B).

    Dùng khi:
    - Tìm A ∪ B.
    - Tìm các phần tử thuộc A hoặc thuộc B.
    - Thực hiện phép hợp giữa hai tập hợp.

    Ví dụ:
    - "Tìm A ∪ B với A={1,2,3}, B={2,3,4}."
    - "Cho hai tập hợp A, B. Tính hợp của chúng."

    Args:
        set_a: các phần tử của tập A, dạng "1,2,3".
        set_b: các phần tử của tập B, dạng "2,3,4".
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        result = sorted(a | b, key=lambda v: float(v))
        return "{" + ", ".join(str(v) for v in result) + "}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def giao_tap_hop_tool(set_a: str, set_b: str) -> str:
    """Tính giao của hai tập hợp (A ∩ B).

    Dùng khi:
    - Tìm A ∩ B.
    - Tìm các phần tử chung của hai tập hợp.
    - Thực hiện phép giao giữa hai tập hợp.

    Ví dụ:
    - "Tìm A ∩ B với A={1,2,3}, B={2,3,4}."
    - "Các phần tử vừa thuộc A vừa thuộc B là gì?"

    Args:
        set_a: các phần tử của tập A, dạng "1,2,3".
        set_b: các phần tử của tập B, dạng "2,3,4".
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        result = sorted(a & b, key=lambda v: float(v))
        return "{" + ", ".join(str(v) for v in result) + "}"
    except Exception as e:
        return f"LOI: {e}"

@tool
def hieu_tap_hop_tool(set_a: str, set_b: str) -> str:
    """Tính hiệu hai tập hợp (A \\ B).

    Dùng khi:
    - Tìm A \\ B.
    - Tìm các phần tử thuộc A nhưng không thuộc B.
    - Thực hiện phép hiệu giữa hai tập hợp.

    Ví dụ:
    - "Tìm A \\ B với A={1,2,3}, B={2,3}."
    - "Phần tử thuộc A mà không thuộc B là gì?"

    Args:
        set_a: các phần tử của tập A, dạng "1,2,3".
        set_b: các phần tử của tập B, dạng "2,3".
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        result = sorted(a - b, key=lambda v: float(v))
        return "{" + ", ".join(str(v) for v in result) + "}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def kiem_tra_tap_con_tool(set_a: str, set_b: str) -> str:
    """Kiểm tra tập hợp A có phải là tập con của tập hợp B hay không.

    Dùng khi:
    - Kiểm tra A ⊂ B.
    - Xét quan hệ tập con giữa hai tập hợp.
    - Chứng minh hoặc xác nhận A có nằm trong B hay không.

    Ví dụ:
    - "A={1,2} có là tập con của B={1,2,3} không?"
    - "Kiểm tra quan hệ tập con giữa A và B."

    Args:
        set_a: các phần tử của tập A.
        set_b: các phần tử của tập B.
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        return str(a.issubset(b))
    except Exception as e:
        return f"LOI: {e}"


# ═══════════════════════════════════════════════════════════════════════
# CHƯƠNG II — Bất phương trình và hệ bất phương trình bậc nhất hai ẩn (c_2)
# ═══════════════════════════════════════════════════════════════════════

@tool
def check_diem_bpt_tool(a: float, b: float, c: float, x0: float, y0: float, sign: str = "<=") -> str:
    """Kiểm tra một điểm có phải là nghiệm của bất phương trình bậc nhất hai ẩn.

    Dùng khi:
    - Kiểm tra điểm M(x0,y0) có thỏa mãn bất phương trình hay không.
    - Xác định một điểm có thuộc miền nghiệm của bất phương trình.
    - Kiểm tra tính đúng sai của một nghiệm được cho trước.

    Ví dụ:
    - "Điểm (1,2) có là nghiệm của 2x+y≤5 không?"
    - "Kiểm tra điểm M(3,1) có thuộc miền nghiệm không?"
    - "Điểm A có thỏa mãn bất phương trình đã cho không?"

    Args:
        a: hệ số của x trong ax+by.
        b: hệ số của y trong ax+by.
        c: hằng số vế phải.
        x0: hoành độ điểm cần kiểm tra.
        y0: tung độ điểm cần kiểm tra.
        sign: dấu bất phương trình ("<=", ">=", "<", ">").
    """
    try:
        value = sp.nsimplify(a) * sp.nsimplify(x0) + sp.nsimplify(b) * sp.nsimplify(y0)
        c_v = sp.nsimplify(c)
        ops = {"<=": value <= c_v, ">=": value >= c_v, "<": value < c_v, ">": value > c_v}
        if sign not in ops:
            return f"LOI: dau khong hop le - {sign}"
        return str(bool(ops[sign]))
    except Exception as e:
        return f"LOI: {e}"


@tool
def tim_gtln_gtnn_mien_tool(a: float, b: float, vertices: str, mode: Literal["max", "min"] = "max") -> str:
    """Tìm GTLN hoặc GTNN của biểu thức F=ax+by trên một miền nghiệm đa giác.

    Dùng khi:
    - Tìm giá trị lớn nhất hoặc nhỏ nhất của F=ax+by.
    - Giải bài toán tối ưu trên miền nghiệm của hệ bất phương trình.
    - Tìm đỉnh của miền nghiệm cho giá trị cực trị.

    Ví dụ:
    - "Tìm GTLN của F=2x+3y trên miền D."
    - "Tìm GTNN của F=x-y trên miền nghiệm."
    - "Giá trị lớn nhất của biểu thức tuyến tính là bao nhiêu?"

    Args:
        a: hệ số của x trong F.
        b: hệ số của y trong F.
        vertices: danh sách các đỉnh miền nghiệm,
            dạng "x1,y1; x2,y2; x3,y3".
        mode: "max" để tìm GTLN, "min" để tìm GTNN.
    """
    try:
        points = []
        for pair in vertices.split(";"):
            xs, ys = pair.strip().split(",")
            points.append((sp.sympify(xs.strip()), sp.sympify(ys.strip())))
        values = [(sp.nsimplify(a) * px + sp.nsimplify(b) * py, (px, py)) for px, py in points]
        best = max(values, key=lambda v: float(v[0])) if mode == "max" else min(values, key=lambda v: float(v[0]))
        return f"F = {best[0]} tai diem ({best[1][0]}, {best[1][1]})"
    except Exception as e:
        return f"LOI: {e}"


@tool
def kiem_tra_he_bpt_tool(x0: float, y0: float, he_bpt: str) -> str:
    """Kiểm tra một điểm có thỏa mãn toàn bộ hệ bất phương trình hay không.

    Dùng khi:
    - Kiểm tra điểm có thuộc miền nghiệm của hệ bất phương trình.
    - Xác định một điểm có là nghiệm của hệ.
    - Đánh giá tính đúng sai của một nghiệm được cho trước.

    Ví dụ:
    - "Điểm (1,1) có là nghiệm của hệ đã cho không?"
    - "Kiểm tra điểm M có thuộc miền nghiệm của hệ."
    - "Điểm A(x,y) có thỏa mãn đồng thời các bất phương trình không?"

    Args:
        x0: hoành độ điểm cần kiểm tra.
        y0: tung độ điểm cần kiểm tra.
        he_bpt: danh sách bất phương trình dạng
            "a1,b1,c1,sign1; a2,b2,c2,sign2; ...".
    """
    try:
        x0_v, y0_v = sp.nsimplify(x0), sp.nsimplify(y0)
        ops = {"<=": lambda v, c: v <= c, ">=": lambda v, c: v >= c, "<": lambda v, c: v < c, ">": lambda v, c: v > c}
        results = []
        for item in he_bpt.split(";"):
            a_s, b_s, c_s, sign = [p.strip() for p in item.strip().split(",")]
            a_v, b_v, c_v = sp.sympify(a_s), sp.sympify(b_s), sp.sympify(c_s)
            value = a_v * x0_v + b_v * y0_v
            if sign not in ops:
                return f"LOI: dau khong hop le - {sign}"
            results.append(bool(ops[sign](value, c_v)))
        return "Đúng (thỏa mãn cả hệ)" if all(results) else f"Sai (không thỏa mãn hệ, chi tiết từng bpt: {results})"
    except Exception as e:
        return f"LOI: {e}"


# ═══════════════════════════════════════════════════════════════════════
# CHƯƠNG III — Hàm số bậc hai và đồ thị (c_3)
# ═══════════════════════════════════════════════════════════════════════
@tool
def tim_txd_ham_so_tool(expression: str, variable: str = "x") -> str:
    """Tìm tập xác định (TXĐ) của một hàm số.

    Dùng khi:
    - Tìm miền xác định của hàm số.
    - Xác định giá trị của biến để hàm có nghĩa.
    - Xét điều kiện xác định của phân thức, căn thức hoặc biểu thức chứa mẫu số.

    Ví dụ:
    - "Tìm TXĐ của y=1/(x-2)."
    - "Hàm số y=sqrt(x-1) xác định khi nào?"
    - "Tìm điều kiện xác định của hàm số."

    Args:
        expression: biểu thức hàm số, ví dụ "1/(x-2)", "sqrt(x-1)".
        variable: tên biến, mặc định là "x".
    """
    try:
        var = sp.symbols(variable)
        expr = sp.sympify(expression)
        domain = continuous_domain(expr, var, sp.S.Reals)
        return str(domain)
    except Exception as e:
        return f"LOI: {e}"


@tool
def xet_bien_thien_tool(expression: str, variable: str = "x", diem_a: float = None, diem_b: float = None) -> str:
    """Xét tính đồng biến hoặc nghịch biến của hàm số trên một khoảng.

    Dùng khi:
    - Xác định khoảng đồng biến, nghịch biến.
    - Xét chiều biến thiên của hàm số.
    - Kiểm tra hàm số tăng hay giảm trên một miền xác định.

    Ví dụ:
    - "Xét tính đồng biến, nghịch biến của y=2x+3."
    - "Hàm số tăng hay giảm trên khoảng (0;5)?"
    - "Cho hàm số, hãy xét sự biến thiên."

    Args:
        expression: biểu thức hàm số, ví dụ "2*x+3", "x**2-4*x+3".
        variable: tên biến, mặc định là "x".
        diem_a: đầu khoảng cần xét.
        diem_b: cuối khoảng cần xét.
    """
    try:
        var = sp.symbols(variable)
        expr = sp.sympify(expression)
        deriv = sp.diff(expr, var)
        mid = (sp.sympify(diem_a) + sp.sympify(diem_b)) / 2
        deriv_val = deriv.subs(var, mid)
        if deriv_val > 0:
            return f"Hàm số đồng biến trên khoảng ({diem_a}, {diem_b}) vì đạo hàm f'(x) = {deriv} > 0 tại điểm giữa khoảng."
        elif deriv_val < 0:
            return f"Hàm số nghịch biến trên khoảng ({diem_a}, {diem_b}) vì đạo hàm f'(x) = {deriv} < 0 tại điểm giữa khoảng."
        else:
            return f"Hàm số không đổi (hằng) trên khoảng ({diem_a}, {diem_b}) vì đạo hàm f'(x) = {deriv} = 0."
    except Exception as e:
        return f"LOI: {e}"


@tool
def tim_dinh_parabol_tool(a: float, b: float, c: float) -> str:
    """Tìm đỉnh và trục đối xứng của parabol y=ax²+bx+c.

    Dùng khi:
    - Tìm tọa độ đỉnh của đồ thị hàm số bậc hai.
    - Xác định trục đối xứng của parabol.
    - Tìm điểm cực đại hoặc cực tiểu của hàm số bậc hai.

    Ví dụ:
    - "Tìm đỉnh của parabol y=x²-4x+3."
    - "Xác định trục đối xứng của đồ thị."
    - "Tìm cực trị của hàm số bậc hai."

    Args:
        a: hệ số bậc hai (a ≠ 0).
        b: hệ số bậc nhất.
        c: hệ số tự do.
    """
    try:
        a_v, b_v, c_v = sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)
        if a_v == 0:
            return "LOI: a phai khac 0"
        x_dinh = -b_v / (2 * a_v)
        y_dinh = c_v - b_v**2 / (4 * a_v)
        huong = "bề lõm hướng lên (a>0), đỉnh là điểm cực tiểu" if a_v > 0 else "bề lõm hướng xuống (a<0), đỉnh là điểm cực đại"
        return f"Đỉnh I({x_dinh}, {y_dinh}). Trục đối xứng: x = {x_dinh}. Đồ thị có {huong}."
    except Exception as e:
        return f"LOI: {e}"


@tool
def xet_dau_tam_thuc_tool(a: float, b: float, c: float) -> str:
    """Xét dấu của tam thức bậc hai f(x)=ax²+bx+c.

    Dùng khi:
    - Xác định khoảng mà f(x) dương hoặc âm.
    - Lập bảng xét dấu tam thức bậc hai.
    - Hỗ trợ giải bất phương trình bậc hai bằng phương pháp xét dấu.

    Ví dụ:
    - "Xét dấu f(x)=x²-5x+6."
    - "Tam thức bậc hai dương khi nào?"
    - "Giải bất phương trình bằng cách xét dấu."

    Args:
        a: hệ số bậc hai (a ≠ 0).
        b: hệ số bậc nhất.
        c: hệ số tự do.
    """
    try:
        a_v, b_v, c_v = sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)
        if a_v == 0:
            return "LOI: a phai khac 0"
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
    except Exception as e:
        return f"LOI: {e}"


# ═══════════════════════════════════════════════════════════════════════
# CHƯƠNG IV — Hệ thức lượng trong tam giác (c_4)
# ═══════════════════════════════════════════════════════════════════════

@tool
def gia_tri_luong_giac_tool(ham: Literal["sin", "cos", "tan", "cot"], goc_do: float) -> str:
    """Tính giá trị lượng giác của một góc từ 0° đến 180°.

    Dùng khi:
    - Tính sin, cos, tan hoặc cot của một góc.
    - Tra giá trị lượng giác của các góc đặc biệt.
    - Thực hiện các bài toán lượng giác cơ bản trong tam giác.

    Ví dụ:
    - "Tính sin150°."
    - "Tính cos120°."
    - "Giá trị tan45° bằng bao nhiêu?"

    Args:
        ham: hàm lượng giác cần tính ("sin", "cos", "tan", "cot").
        goc_do: số đo góc theo độ.
    """
    try:
        rad = _deg(goc_do)
        funcs = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "cot": sp.cot}
        if ham not in funcs:
            return f"LOI: ham khong hop le - {ham}"
        val = sp.trigsimp(funcs[ham](rad))
        return f"{ham}({sp.nsimplify(goc_do)}°) = {val} ≈ {float(val):.4f}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def dinh_ly_cosin_tool(
    operation: Literal["tinh_canh", "tinh_goc"],
    a: float = None, b: float = None, c: float = None, goc_a_do: float = None,
) -> str:
    """Áp dụng định lý côsin để tính cạnh hoặc góc trong tam giác.

    Dùng khi:
    - Biết hai cạnh và góc xen giữa, cần tính cạnh còn lại.
    - Biết ba cạnh, cần tính một góc của tam giác.
    - Giải tam giác bằng định lý côsin.

    Ví dụ:
    - "Cho b=5, c=7, góc A=60°. Tính cạnh a."
    - "Biết ba cạnh a, b, c. Tính góc A."
    - "Áp dụng định lý côsin để giải tam giác."

    Args:
        operation: "tinh_canh" hoặc "tinh_goc".
        a: cạnh a (dùng khi tính góc).
        b: cạnh b.
        c: cạnh c.
        goc_a_do: góc A theo độ (dùng khi tính cạnh).
    """
    try:
        if operation == "tinh_canh":
            b_v, c_v = sp.nsimplify(b), sp.nsimplify(c)
            rad = _deg(goc_a_do)
            a2 = b_v**2 + c_v**2 - 2 * b_v * c_v * sp.cos(rad)
            a_val = sp.sqrt(sp.simplify(a2))
            return f"Cạnh a = √(b²+c²-2bc.cosA) = {a_val} ≈ {float(a_val):.4f}"
        elif operation == "tinh_goc":
            a_v, b_v, c_v = sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)
            cos_a = (b_v**2 + c_v**2 - a_v**2) / (2 * b_v * c_v)
            goc = _to_deg(sp.acos(sp.simplify(cos_a)))
            return f"cosA = {sp.simplify(cos_a)}, góc A ≈ {float(goc):.2f}°"
        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def dinh_ly_sin_tool(
    operation: Literal["tinh_canh_goc", "tinh_ban_kinh"],
    a: float = None, goc_a_do: float = None, goc_b_do: float = None,
) -> str:
    """Áp dụng định lý sin để tính cạnh, góc hoặc bán kính ngoại tiếp.

    Dùng khi:
    - Tính cạnh còn lại khi biết một cạnh và các góc liên quan.
    - Tính bán kính đường tròn ngoại tiếp tam giác.
    - Giải tam giác bằng định lý sin.

    Ví dụ:
    - "Biết a=6, góc A=45°, góc B=60°. Tính cạnh b."
    - "Biết a và góc A. Tính bán kính ngoại tiếp R."
    - "Áp dụng định lý sin để tìm cạnh chưa biết."

    Args:
        operation: "tinh_canh_goc" hoặc "tinh_ban_kinh".
        a: cạnh a.
        goc_a_do: góc A theo độ.
        goc_b_do: góc B theo độ (dùng khi tính cạnh).
    """
    try:
        a_v = sp.nsimplify(a)
        rad_a = _deg(goc_a_do)
        if operation == "tinh_canh_goc":
            rad_b = _deg(goc_b_do)
            b_val = a_v * sp.sin(rad_b) / sp.sin(rad_a)
            return f"Cạnh b = a.sinB/sinA = {sp.simplify(b_val)} ≈ {float(b_val):.4f}"
        elif operation == "tinh_ban_kinh":
            r_val = a_v / (2 * sp.sin(rad_a))
            return f"Bán kính đường tròn ngoại tiếp R = a/(2sinA) = {sp.simplify(r_val)} ≈ {float(r_val):.4f}"
        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def giai_tam_giac_tool(
    operation: Literal["biet_2_canh_1_goc_xen_giua", "biet_1_canh_2_goc"],
    b: float = None, c: float = None, goc_a_do: float = None,
    a: float = None, goc_b_do: float = None,
) -> str:
    """Giải tam giác khi biết một số yếu tố ban đầu.

    Dùng khi:
    - Tìm các cạnh và góc còn lại của tam giác.
    - Giải tam giác từ hai cạnh và góc xen giữa.
    - Giải tam giác từ một cạnh và hai góc.

    Ví dụ:
    - "Biết b, c và góc A. Giải tam giác."
    - "Biết a, góc A, góc B. Tìm các yếu tố còn lại."
    - "Hoàn chỉnh các cạnh và góc của tam giác."

    Args:
        operation: phương án dữ liệu đầu vào của bài toán.
        b: cạnh b.
        c: cạnh c.
        goc_a_do: góc A theo độ.
        a: cạnh a.
        goc_b_do: góc B theo độ.
    """
    try:
        if operation == "biet_2_canh_1_goc_xen_giua":
            b_v, c_v = sp.nsimplify(b), sp.nsimplify(c)
            rad_a = _deg(goc_a_do)
            a2 = b_v**2 + c_v**2 - 2 * b_v * c_v * sp.cos(rad_a)
            a_val = float(sp.sqrt(sp.simplify(a2)))
            sin_b = float(b_v) * sp.sin(rad_a) / a_val
            goc_b = float(_to_deg(sp.asin(sin_b)))
            goc_c = 180 - float(goc_a_do) - goc_b
            return f"a ≈ {a_val:.4f}, góc B ≈ {goc_b:.2f}°, góc C ≈ {goc_c:.2f}°"
        elif operation == "biet_1_canh_2_goc":
            a_v = sp.nsimplify(a)
            rad_a, rad_b = _deg(goc_a_do), _deg(goc_b_do)
            goc_c_do = 180 - float(goc_a_do) - float(goc_b_do)
            rad_c = _deg(goc_c_do)
            b_val = float(a_v * sp.sin(rad_b) / sp.sin(rad_a))
            c_val = float(a_v * sp.sin(rad_c) / sp.sin(rad_a))
            return f"góc C ≈ {goc_c_do:.2f}°, cạnh b ≈ {b_val:.4f}, cạnh c ≈ {c_val:.4f}"
        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def dien_tich_tam_giac_tool(
    operation: Literal["heron", "luong_giac"],
    a: float = None, b: float = None, c: float = None, goc_c_do: float = None,
) -> str:
    """Tính diện tích tam giác bằng công thức Heron hoặc công thức lượng giác.

    Dùng khi:
    - Tính diện tích tam giác từ ba cạnh.
    - Tính diện tích khi biết hai cạnh và góc xen giữa.
    - Lựa chọn công thức phù hợp theo dữ kiện đề bài.

    Ví dụ:
    - "Biết a=3, b=4, c=5. Tính diện tích tam giác."
    - "Biết a=5, b=6, góc C=60°. Tính diện tích."
    - "Áp dụng công thức Heron để tính diện tích."

    Args:
        operation: "heron" hoặc "luong_giac".
        a: cạnh a.
        b: cạnh b.
        c: cạnh c (dùng cho Heron).
        goc_c_do: góc C theo độ (dùng cho công thức lượng giác).
    """
    try:
        if operation == "heron":
            a_v, b_v, c_v = sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)
            s = (a_v + b_v + c_v) / 2
            area = sp.sqrt(s * (s - a_v) * (s - b_v) * (s - c_v))
            return f"S = √(p(p-a)(p-b)(p-c)) = {sp.simplify(area)} ≈ {float(area):.4f}"
        elif operation == "luong_giac":
            a_v, b_v = sp.nsimplify(a), sp.nsimplify(b)
            rad_c = _deg(goc_c_do)
            area = sp.Rational(1, 2) * a_v * b_v * sp.sin(rad_c)
            return f"S = (1/2).a.b.sinC = {sp.simplify(area)} ≈ {float(area):.4f}"
        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"
# ═══════════════════════════════════════════════════════════════════════
# CHƯƠNG V — Vectơ (c_5)
# ═══════════════════════════════════════════════════════════════════════
@tool
def tong_hieu_vecto_tool(
    vecto_a: str,
    vecto_b: str,
    operation: Literal["tong", "hieu"] = "tong"
) -> str:
    """Tính tổng hoặc hiệu của hai vectơ theo tọa độ.

    Dùng khi:
    - Tính a+b hoặc a-b.
    - Thực hiện các phép toán cộng, trừ vectơ.
    - Tìm vectơ kết quả từ hai vectơ đã biết.

    Ví dụ:
    - "Cho a=(1,2), b=(3,-1). Tính a+b."
    - "Cho a và b. Tính a-b."
    - "Tìm vectơ tổng của hai vectơ."

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y".
        vecto_b: tọa độ vectơ b, dạng "x,y".
        operation: "tong" hoặc "hieu".
    """
    try:
        ax, ay = _parse_vector(vecto_a)
        bx, by = _parse_vector(vecto_b)
        if operation == "tong":
            return f"a + b = ({ax + bx}, {ay + by})"
        elif operation == "hieu":
            return f"a - b = ({ax - bx}, {ay - by})"
        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def tich_so_voi_vecto_tool(vecto_a: str, k: float) -> str:
    """Tính tích của một số thực với một vectơ.

    Dùng khi:
    - Nhân vectơ với một số thực.
    - Tìm tọa độ vectơ k.a.
    - Xác định vectơ cùng phương hoặc ngược phương với vectơ đã cho.

    Ví dụ:
    - "Cho a=(2,3). Tính 3a."
    - "Nhân vectơ a với hệ số k."
    - "Tìm tọa độ của k.a."

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y".
        k: số thực nhân với vectơ.
    """
    try:
        ax, ay = _parse_vector(vecto_a)
        k_v = sp.nsimplify(k)
        return f"{k_v}.a = ({k_v * ax}, {k_v * ay})"
    except Exception as e:
        return f"LOI: {e}"


@tool
def tich_vo_huong_vecto_tool(vecto_a: str, vecto_b: str) -> str:
    """Tính tích vô hướng của hai vectơ theo tọa độ.

    Dùng khi:
    - Tính a·b.
    - Kiểm tra hai vectơ có vuông góc hay không.
    - Hỗ trợ tính góc giữa hai vectơ.

    Ví dụ:
    - "Cho a=(1,2), b=(3,-4). Tính a·b."
    - "Hai vectơ có vuông góc không?"
    - "Tính tích vô hướng của hai vectơ."

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y".
        vecto_b: tọa độ vectơ b, dạng "x,y".
    """
    try:
        ax, ay = _parse_vector(vecto_a)
        bx, by = _parse_vector(vecto_b)
        dot = ax * bx + ay * by
        return f"a·b = {dot}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def do_dai_vecto_tool(vecto_a: str) -> str:
    """Tính độ dài (độ lớn) của một vectơ.

    Dùng khi:
    - Tính |a|.
    - Tìm độ lớn của vectơ theo tọa độ.
    - Tính khoảng cách hoặc độ dài đoạn thẳng từ vectơ chỉ phương.

    Ví dụ:
    - "Cho a=(3,4). Tính |a|."
    - "Tìm độ dài vectơ a."
    - "Độ lớn của vectơ bằng bao nhiêu?"

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y".
    """
    try:
        ax, ay = _parse_vector(vecto_a)
        length = sp.sqrt(ax**2 + ay**2)
        return f"|a| = √(x²+y²) = {sp.simplify(length)} ≈ {float(length):.4f}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def goc_giua_hai_vecto_tool(vecto_a: str, vecto_b: str) -> str:
    """Tính góc giữa hai vectơ bằng tích vô hướng.

    Dùng khi:
    - Tính góc giữa hai vectơ.
    - Xác định độ lệch hướng giữa hai vectơ.
    - Kiểm tra quan hệ vuông góc hoặc song song thông qua góc.

    Ví dụ:
    - "Cho a=(1,0), b=(0,1). Tính góc giữa a và b."
    - "Tìm góc tạo bởi hai vectơ."
    - "Hai vectơ hợp với nhau góc bao nhiêu độ?"

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y".
        vecto_b: tọa độ vectơ b, dạng "x,y".
    """
    try:
        ax, ay = _parse_vector(vecto_a)
        bx, by = _parse_vector(vecto_b)
        dot = ax * bx + ay * by
        len_a = sp.sqrt(ax**2 + ay**2)
        len_b = sp.sqrt(bx**2 + by**2)
        if len_a == 0 or len_b == 0:
            return "LOI: vecto khong duoc la vecto khong"
        cos_goc = dot / (len_a * len_b)
        goc = _to_deg(sp.acos(sp.simplify(cos_goc)))
        return f"cos(a,b) = {sp.simplify(cos_goc)}, góc giữa a và b ≈ {float(goc):.2f}°"
    except Exception as e:
        return f"LOI: {e}"

# ═══════════════════════════════════════════════════════════════════════
# CHƯƠNG VI — Thống kê (c_6)
# ═══════════════════════════════════════════════════════════════════════
@tool
def sai_so_tuong_doi_tool(
    operation: Literal["tuyet_doi", "tuong_doi"],
    so_gan_dung: float,
    so_dung: float = None,
    sai_so_tuyet_doi_da_biet: float = None,
) -> str:
    """Tính sai số tuyệt đối hoặc sai số tương đối của một số gần đúng.

    Dùng khi:
    - Tính sai số tuyệt đối giữa giá trị gần đúng và giá trị đúng.
    - Tính sai số tương đối hoặc phần trăm sai số.
    - Đánh giá độ chính xác của kết quả đo đạc hoặc tính toán.

    Ví dụ:
    - "Tính sai số tuyệt đối của số gần đúng 3.14."
    - "Tính sai số tương đối của kết quả đo."
    - "Độ chính xác của số gần đúng là bao nhiêu?"

    Args:
        operation: "tuyet_doi" hoặc "tuong_doi".
        so_gan_dung: giá trị gần đúng.
        so_dung: giá trị đúng (nếu biết).
        sai_so_tuyet_doi_da_biet: sai số tuyệt đối đã biết trước.
    """
    try:
        a_v = sp.nsimplify(so_gan_dung)
        if operation == "tuyet_doi":
            if so_dung is None:
                return "LOI: can gia tri so_dung de tinh sai so tuyet doi"
            delta = sp.Abs(sp.nsimplify(so_dung) - a_v)
            return f"Sai số tuyệt đối = |số đúng - số gần đúng| = {sp.simplify(delta)} ≈ {float(delta):.6f}"
        elif operation == "tuong_doi":
            if so_dung is not None:
                delta = sp.Abs(sp.nsimplify(so_dung) - a_v)
            elif sai_so_tuyet_doi_da_biet is not None:
                delta = sp.nsimplify(sai_so_tuyet_doi_da_biet)
            else:
                return "LOI: can so_dung hoac sai_so_tuyet_doi_da_biet"
            rel = delta / sp.Abs(a_v)
            return f"Sai số tương đối = {sp.simplify(rel)} ≈ {float(rel) * 100:.4f}%"
        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def tinh_trung_binh_tool(so_lieu: str) -> str:
    """Tính số trung bình của một mẫu số liệu.

    Dùng khi:
    - Tính giá trị trung bình cộng của dữ liệu.
    - Xác định giá trị đại diện cho mẫu số liệu.
    - Thống kê xu hướng trung tâm của dữ liệu.

    Ví dụ:
    - "Tính số trung bình của mẫu số liệu."
    - "Tìm giá trị trung bình cộng."
    - "Điểm trung bình của nhóm là bao nhiêu?"

    Args:
        so_lieu: các giá trị số liệu, cách nhau bởi dấu phẩy.
    """
    try:
        nums = _parse_numbers(so_lieu)
        mean = sum(nums) / len(nums)
        return f"Số trung bình = {sp.simplify(mean)} ≈ {float(mean):.4f}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def tinh_trung_vi_mode_tool(
    so_lieu: str,
    operation: Literal["trung_vi", "mode"] = "trung_vi"
) -> str:
    """Tính số trung vị hoặc mốt của một mẫu số liệu.

    Dùng khi:
    - Tìm trung vị của dãy số liệu.
    - Tìm mốt (giá trị xuất hiện nhiều nhất).
    - Mô tả đặc trưng trung tâm của dữ liệu.

    Ví dụ:
    - "Tính trung vị của mẫu số liệu."
    - "Tìm mốt của dãy số."
    - "Giá trị xuất hiện nhiều nhất là gì?"

    Args:
        so_lieu: các giá trị số liệu, cách nhau bởi dấu phẩy.
        operation: "trung_vi" hoặc "mode".
    """
    try:
        nums = _parse_numbers(so_lieu)
        if operation == "trung_vi":
            sorted_nums = sorted(nums, key=lambda v: float(v))
            n = len(sorted_nums)
            if n % 2 == 1:
                med = sorted_nums[n // 2]
            else:
                med = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2
            return f"Số trung vị = {sp.simplify(med)}"
        elif operation == "mode":
            from collections import Counter
            counts = Counter(nums)
            max_count = max(counts.values())
            modes = [str(v) for v, c in counts.items() if c == max_count]
            return f"Mốt = {', '.join(modes)} (xuất hiện {max_count} lần)"
        return f"LOI: operation khong hop le - {operation}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def tinh_phuong_sai_do_lech_chuan_tool(so_lieu: str) -> str:
    """Tính phương sai và độ lệch chuẩn của một mẫu số liệu.

    Dùng khi:
    - Đo mức độ phân tán của dữ liệu.
    - Tính phương sai của mẫu số liệu.
    - Tính độ lệch chuẩn để đánh giá độ biến động.

    Ví dụ:
    - "Tính phương sai của mẫu số liệu."
    - "Tính độ lệch chuẩn của dãy số."
    - "Dữ liệu phân tán nhiều hay ít?"

    Args:
        so_lieu: các giá trị số liệu, cách nhau bởi dấu phẩy.
    """
    try:
        nums = _parse_numbers(so_lieu)
        n = len(nums)
        mean = sum(nums) / n
        variance = sum((v - mean) ** 2 for v in nums) / n
        std = sp.sqrt(variance)
        return f"Phương sai = {sp.simplify(variance)} ≈ {float(variance):.4f}. Độ lệch chuẩn = {sp.simplify(std)} ≈ {float(std):.4f}"
    except Exception as e:
        return f"LOI: {e}"


# ═══════════════════════════════════════════════════════════════════════
# Tổng hợp tool + map tên → hàm (dùng để tra cứu sau khi rerank theo tool_name)
# ═══════════════════════════════════════════════════════════════════════

MATH_TOOLS_V2 = [
    xet_menh_de_tool, phu_dinh_menh_de_tool, hop_tap_hop_tool, giao_tap_hop_tool,
    hieu_tap_hop_tool, kiem_tra_tap_con_tool,
    check_diem_bpt_tool, tim_gtln_gtnn_mien_tool, kiem_tra_he_bpt_tool,
    tim_txd_ham_so_tool, xet_bien_thien_tool, tim_dinh_parabol_tool, xet_dau_tam_thuc_tool,
    gia_tri_luong_giac_tool, dinh_ly_cosin_tool, dinh_ly_sin_tool, giai_tam_giac_tool, dien_tich_tam_giac_tool,
    tong_hieu_vecto_tool, tich_so_voi_vecto_tool, tich_vo_huong_vecto_tool, do_dai_vecto_tool, goc_giua_hai_vecto_tool,
    sai_so_tuong_doi_tool, tinh_trung_binh_tool, tinh_trung_vi_mode_tool, tinh_phuong_sai_do_lech_chuan_tool,
]

TOOL_MAP_V2 = {t.name: t for t in MATH_TOOLS_V2}

print(f"math_tools_v2.py loaded successfully — {len(MATH_TOOLS_V2)} tools")