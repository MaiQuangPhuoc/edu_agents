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
    """Xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.

    Dùng khi đề bài hỏi dạng: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của
    câu sau", "khẳng định sau đúng hay sai?", kể cả khi câu hỏi diễn đạt qua tình
    huống thực tế (vd tính chất chia hết, tính chẵn lẻ, so sánh số) chứ không chỉ
    hỏi trực tiếp bằng công thức.

    Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
    Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

    Args:
        bieu_thuc: biểu thức logic/so sánh dạng Python-SymPy, ví dụ "15 % 3 == 0",
            "Eq(2+2, 4)", "sqrt(4) == 2". Dùng ==, !=, >, <, >=, <= để so sánh.
    """
    try:
        expr = sp.sympify(bieu_thuc)
        result = bool(expr)
        return "Đúng" if result else "Sai"
    except Exception as e:
        return f"LOI: {e}"

@tool
def phu_dinh_menh_de_tool(bieu_thuc: str) -> str:
    """Viết mệnh đề phủ định của 1 mệnh đề cho trước.

    Dùng khi đề bài yêu cầu: "viết mệnh đề phủ định của P", "phủ định của mệnh đề
    sau là gì", "lập mệnh đề phủ định", kể cả khi mệnh đề gốc chứa lượng từ "mọi",
    "tồn tại" hoặc mô tả bằng lời (không chỉ ký hiệu toán học thuần túy).

    Ví dụ: phủ định của "Mọi số tự nhiên đều lớn hơn 0" là "Tồn tại số tự nhiên nhỏ
    hơn hoặc bằng 0".
    Ví dụ: phủ định của "n chia hết cho 5" là "n không chia hết cho 5".

    Args:
        bieu_thuc: biểu thức so sánh dạng SymPy, ví dụ "x > 3", "Eq(x, 5)".
            Tool sẽ trả về biểu thức phủ định (đảo dấu so sánh).
    """
    try:
        expr = sp.sympify(bieu_thuc)
        neg = sp.Not(expr) if not isinstance(expr, sp.core.relational.Relational) else ~expr
        return str(neg)
    except Exception as e:
        return f"LOI: {e}"

@tool
def hop_tap_hop_tool(set_a: str, set_b: str) -> str:
    """Tính hợp (union, A ∪ B) của hai tập hợp số.

    Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng: "tìm A ∪ B", "tập hợp gồm
    các phần tử thuộc A hoặc thuộc B", kể cả khi 2 tập hợp được mô tả qua tình
    huống thực tế (vd nhóm học sinh giỏi 2 môn khác nhau, danh sách khách hàng mua
    2 loại sản phẩm khác nhau) chứ không chỉ liệt kê số thuần túy.

    Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
    Ví dụ: "Lớp có tập học sinh giỏi Toán A={1,2,3} và giỏi Văn B={2,4}, tìm tập
    học sinh giỏi Toán hoặc giỏi Văn" → A ∪ B = {1,2,3,4}.

    Args:
        set_a: các phần tử tập A, cách nhau bởi dấu phẩy, ví dụ "1, 2, 3".
        set_b: các phần tử tập B, cách nhau bởi dấu phẩy.
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        result = sorted(a | b, key=lambda v: float(v))
        return "{" + ", ".join(str(v) for v in result) + "}"
    except Exception as e:
        return f"LOI: {e}"

@tool
def giao_tap_hop_tool(set_a: str, set_b: str) -> str:
    """Tính giao (intersection, A ∩ B) của hai tập hợp số.

    Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung: "tìm A ∩ B", "tập hợp
    gồm các phần tử vừa thuộc A vừa thuộc B", kể cả khi 2 tập hợp mô tả qua tình
    huống thực tế (vd học sinh đạt giỏi cả 2 môn, ước chung của 2 số) chứ không
    chỉ liệt kê số thuần túy.

    Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.
    Ví dụ: "Tìm mức điểm đạt giỏi cả Toán và Văn, biết A={5,...,10} là điểm giỏi
    Toán, B={7,...,11} là điểm giỏi Văn" → A ∩ B = {7,8,9,10}.

    Args:
        set_a: các phần tử tập A, cách nhau bởi dấu phẩy, ví dụ "1, 2, 3".
        set_b: các phần tử tập B, cách nhau bởi dấu phẩy.
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        result = sorted(a & b, key=lambda v: float(v))
        return "{" + ", ".join(str(v) for v in result) + "}"
    except Exception as e:
        return f"LOI: {e}"

@tool
def hieu_tap_hop_tool(set_a: str, set_b: str) -> str:
    """Tính hiệu (difference, A \\ B) của hai tập hợp số — các phần tử thuộc A
    nhưng không thuộc B.

    Dùng khi đề bài hỏi "tìm A \\ B", "phần tử thuộc A mà không thuộc B", kể cả
    khi diễn đạt qua tình huống thực tế (vd khách chỉ mua sản phẩm này mà không
    mua sản phẩm kia) chứ không chỉ liệt kê số thuần túy.

    Ví dụ: "Tìm A \\ B với A={1,2,3}, B={2,3}" → A \\ B = {1}.
    Ví dụ: "Khách mua áo A={1,...,6}, khách mua quần B={4,5,6}, tìm khách chỉ mua
    áo mà không mua quần" → A \\ B = {1,2,3}.

    Args:
        set_a: các phần tử tập A, cách nhau bởi dấu phẩy, ví dụ "1, 2, 3".
        set_b: các phần tử tập B, cách nhau bởi dấu phẩy.
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        result = sorted(a - b, key=lambda v: float(v))
        return "{" + ", ".join(str(v) for v in result) + "}"
    except Exception as e:
        return f"LOI: {e}"

@tool
def kiem_tra_tap_con_tool(set_a: str, set_b: str) -> str:
    """Kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).

    Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B",
    "kiểm tra quan hệ tập con", kể cả khi A, B là tập nghiệm phương trình, tập
    ước số, hoặc mô tả qua tình huống thực tế (vd học sinh giỏi là tập con của
    toàn bộ học sinh lớp) chứ không chỉ liệt kê số thuần túy.

    Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).
    Ví dụ: "Tập nghiệm của x²=4 là A={-2,2}, B={-2,-1,0,1,2}, A có là tập con
    của B không?" → Đúng (True).

    Args:
        set_a: các phần tử tập A, cách nhau bởi dấu phẩy.
        set_b: các phần tử tập B, cách nhau bởi dấu phẩy.
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
    """Kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn
    ax + by (dấu) c hay không.

    Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau
    không?", "kiểm tra điểm sau có thuộc miền nghiệm không", kể cả khi điểm được
    mô tả qua tình huống thực tế (vd phương án sản xuất (x,y) có thỏa ràng buộc
    nguyên liệu không, phương án phân bổ có khả thi không) chứ không chỉ hỏi
    trực tiếp bằng tọa độ và công thức thuần túy.

    Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.
    Ví dụ: "Một xưởng cần thỏa ràng buộc nguyên liệu 2x+3y≤120, kiểm tra phương
    án sản xuất (x=30,y=20) có khả thi không" → 2*30+3*20=120 ≤ 120 → Đúng.

    Args:
        a: hệ số của x.
        b: hệ số của y.
        c: hằng số vế phải.
        x0: hoành độ điểm cần kiểm tra.
        y0: tung độ điểm cần kiểm tra.
        sign: dấu bất phương trình, 1 trong "<=", ">=", "<", ">".
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
    """Tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức
    F = ax + by trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).

    Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy
    hoạch tuyến tính, tối ưu hóa với ràng buộc là hệ bất phương trình, kể cả khi
    F được mô tả qua tình huống thực tế (vd lợi nhuận công ty, doanh thu, chi
    phí cần tối ưu trên 1 miền ràng buộc sản xuất) chứ không chỉ hỏi trực tiếp
    bằng công thức F=ax+by thuần túy.

    Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".
    Ví dụ: "Công ty sản xuất 2 sản phẩm với lợi nhuận F=5x+4y, miền ràng buộc có
    đỉnh (0,0),(20,0),(15,10),(0,15). Tìm phương án cho lợi nhuận GTLN".

    Args:
        a: hệ số của x trong F.
        b: hệ số của y trong F.
        vertices: tọa độ các đỉnh đa giác, dạng "x1,y1; x2,y2; x3,y3".
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
    """Kiểm tra 1 điểm (x0, y0) có thỏa mãn ĐỒNG THỜI tất cả các bất phương
    trình trong 1 hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền
    nghiệm của hệ hay không).

    Dùng khi đề bài cho NHIỀU bất phương trình cùng lúc (hệ, thường có từ 2 ràng
    buộc trở lên, ví dụ kèm cả x≥0, y≥0) và hỏi 1 điểm có là nghiệm của hệ đó
    không — khác với check_diem_bpt_tool chỉ kiểm tra 1 bất phương trình đơn lẻ.
    Kể cả khi điểm là phương án thực tế (vd phương án sản xuất, phân bổ nguồn
    lực có thỏa tất cả ràng buộc không) chứ không chỉ hỏi trực tiếp bằng tọa độ.

    Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra
    từng bpt trong hệ.
    Ví dụ: "Phương án sản xuất (x=10,y=5) có thỏa hệ ràng buộc {x+2y≤25;
    3x+y≤40; x≥0; y≥0} không?" → kiểm tra đồng thời cả 4 ràng buộc.

    Args:
        x0: hoành độ điểm cần kiểm tra.
        y0: tung độ điểm cần kiểm tra.
        he_bpt: danh sách các bất phương trình trong hệ, dạng
            "a1,b1,c1,sign1; a2,b2,c2,sign2; ...", ví dụ
            "1,1,3,<=; 1,-1,-2,>=; 1,0,0,>=".
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
    """Tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức,
    đa thức).

    Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi
    nào", kể cả khi hàm số mô tả 1 đại lượng thực tế (vd chi phí sản xuất theo
    số lượng sản phẩm x) và cần tìm miền giá trị x hợp lệ, chứ không chỉ hỏi
    trực tiếp bằng biểu thức toán học thuần túy.

    Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \\ {2}.
    Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).
    Ví dụ: "Chi phí sản xuất y=1000/(x-10), tìm tập xác định để biết giá trị x
    hợp lệ" → D = R \\ {10}.

    Args:
        expression: biểu thức hàm số, ví dụ "1/(x-2)", "sqrt(x-1)".
        variable: biến số, mặc định "x".
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
    """Xét tính đồng biến, nghịch biến của hàm số trên khoảng (diem_a, diem_b).

    Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào",
    "xét sự biến thiên của hàm số", kể cả khi hàm số mô tả 1 đại lượng thực tế
    theo thời gian (vd doanh thu theo tháng, quãng đường theo thời gian) và cần
    biết xu hướng tăng/giảm, chứ không chỉ hỏi trực tiếp bằng biểu thức thuần
    túy.

    Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ
    số góc >0.
    Ví dụ: "Doanh thu cửa hàng theo tháng là y=200x+1000, xét hàm số đồng biến
    hay nghịch biến trên (1,12) để biết xu hướng doanh thu" → đồng biến.

    Args:
        expression: biểu thức hàm số, ví dụ "2*x+3", "x**2-4*x+3".
        variable: biến số, mặc định "x".
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
    """Tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.

    Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm
    số bậc hai là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai", kể cả
    khi hàm số mô tả 1 tình huống thực tế (vd quỹ đạo vật ném lên theo thời
    gian, cần tìm thời điểm và độ cao lớn nhất) chứ không chỉ hỏi trực tiếp
    bằng công thức thuần túy.

    Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.
    Ví dụ: "Quỹ đạo vật ném lên y=-5x²+20x (x là thời gian, y là độ cao), tìm
    đỉnh parabol để biết thời điểm và độ cao lớn nhất" → Đỉnh I(2, 20).

    Args:
        a: hệ số bậc 2 (khác 0).
        b: hệ số bậc 1.
        c: hằng số.
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
    """Xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.

    Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất
    phương trình bậc hai" (thông qua xét dấu), kể cả khi f(x) mô tả 1 đại lượng
    thực tế theo sản lượng/số lượng (vd lợi nhuận công ty theo sản lượng x, cần
    biết khoảng nào có lãi) chứ không chỉ hỏi trực tiếp bằng công thức thuần
    túy.

    Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi
    2<x<3.
    Ví dụ: "Lợi nhuận công ty theo sản lượng x là f(x)=-x²+10x-16, xét dấu f(x)
    để biết khoảng sản lượng nào công ty có lãi" → có lãi khi 2<x<8.

    Args:
        a: hệ số bậc 2 (khác 0).
        b: hệ số bậc 1.
        c: hằng số.
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
    """Tính giá trị lượng giác (sin, cos, tan, cot) của 1 góc từ 0° đến 180°.

    Dùng khi đề bài hỏi: "tính sin/cos/tan/cot của góc α", "giá trị lượng giác
    của góc 120° là bao nhiêu", kể cả khi góc xuất hiện qua tình huống thực tế
    (vd góc nghiêng mái nhà, góc giữa 2 hướng đi) chứ không chỉ hỏi trực tiếp
    "tính sin/cos của góc X°".

    Ví dụ: "Tính sin150°" → sin150° = 1/2.
    Ví dụ: "Tính cos120°" → cos120° = -1/2.
    Ví dụ: "Mái nhà nghiêng tạo với phương ngang một góc 120°, tính cos của góc
    này" → cos120° = -1/2.

    Args:
        ham: loại hàm lượng giác cần tính, 1 trong "sin", "cos", "tan", "cot".
        goc_do: số đo góc theo độ, ví dụ 150.
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
    """Áp dụng định lí côsin: tính 1 cạnh khi biết 2 cạnh + góc xen giữa, hoặc
    tính góc khi biết 3 cạnh. Công thức: a² = b² + c² - 2bc.cosA.

    Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa (hỏi cạnh còn lại),
    hoặc biết 3 cạnh (hỏi 1 góc), kể cả khi tam giác mô tả qua tình huống thực
    tế (vd khoảng cách giữa 2 con tàu xuất phát cùng điểm theo 2 hướng khác
    nhau) chứ không chỉ hỏi trực tiếp bằng cạnh/góc thuần túy.

    Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".
    Ví dụ: "Hai con tàu xuất phát từ cùng 1 điểm, tàu 1 đi 5km, tàu 2 đi 8km,
    góc giữa 2 hướng đi là 70°. Tính khoảng cách giữa hai tàu" → dùng định lí
    cosin với b=5, c=8, góc A=70°.

    Args:
        operation: "tinh_canh" (biết b, c, góc A tính cạnh a) hoặc "tinh_goc"
            (biết a, b, c tính góc A).
        a: cạnh a (dùng cho tinh_goc, hoặc là kết quả cần tìm ở tinh_canh nên
            để trống).
        b: cạnh b.
        c: cạnh c.
        goc_a_do: góc A tính bằng độ (dùng cho tinh_canh, là góc xen giữa b và c).
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
    """Áp dụng định lí sin: tính cạnh/góc khác, hoặc tính bán kính đường tròn
    ngoại tiếp tam giác. Công thức: a/sinA = b/sinB = c/sinC = 2R.

    Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính
    R, kể cả khi tam giác mô tả qua tình huống thực tế (vd khu đất tam giác
    nhìn dưới 1 góc, cần tính bán kính đường tròn ngoại tiếp khu đất) chứ không
    chỉ hỏi trực tiếp bằng cạnh/góc thuần túy.

    Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp
    R".
    Ví dụ: "Một khu đất tam giác có cạnh a=15m nhìn dưới góc A=35°. Tính bán
    kính đường tròn ngoại tiếp khu đất" → dùng định lí sin.

    Args:
        operation: "tinh_canh_goc" (biết a, góc A, góc B, tính cạnh b) hoặc
            "tinh_ban_kinh" (biết a, góc A, tính bán kính R).
        a: cạnh a.
        goc_a_do: góc A tính bằng độ, đối diện cạnh a.
        goc_b_do: góc B tính bằng độ, đối diện cạnh cần tìm (chỉ dùng cho
            tinh_canh_goc).
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
    """Giải tam giác — tìm toàn bộ cạnh và góc còn lại khi biết 1 số yếu tố ban đầu.

    Args:
        operation: "biet_2_canh_1_goc_xen_giua" (biết b, c, góc A) hoặc
            "biet_1_canh_2_goc" (biết a, góc A, góc B).
        b: cạnh b (dùng cho biet_2_canh_1_goc_xen_giua).
        c: cạnh c (dùng cho biet_2_canh_1_goc_xen_giua).
        goc_a_do: góc A tính bằng độ.
        a: cạnh a (dùng cho biet_1_canh_2_goc).
        goc_b_do: góc B tính bằng độ (dùng cho biet_1_canh_2_goc).
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
    """Tính diện tích tam giác bằng công thức Heron (biết 3 cạnh) hoặc công thức lượng giác (biết 2 cạnh + góc xen giữa).

    Args:
        operation: "heron" (biết a, b, c) hoặc "luong_giac" (biết a, b, góc C xen giữa).
        a: cạnh a.
        b: cạnh b.
        c: cạnh c (dùng cho heron).
        goc_c_do: góc C tính bằng độ, xen giữa cạnh a và b (dùng cho luong_giac).
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
def tong_hieu_vecto_tool(vecto_a: str, vecto_b: str, operation: Literal["tong", "hieu"] = "tong") -> str:
    """Tính tổng (a+b) hoặc hiệu (a-b) của hai vectơ theo tọa độ.

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y", ví dụ "1,2".
        vecto_b: tọa độ vectơ b, dạng "x,y".
        operation: "tong" để tính a+b, "hieu" để tính a-b.
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
    """Tính tích của 1 số thực k với 1 vectơ a (k.a) theo tọa độ.

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y", ví dụ "2,3".
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
    """Tính tích vô hướng (dot product) của hai vectơ theo tọa độ.

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y", ví dụ "1,2".
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
    """Tính độ dài (độ lớn) của 1 vectơ theo tọa độ.

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y", ví dụ "3,4".
    """
    try:
        ax, ay = _parse_vector(vecto_a)
        length = sp.sqrt(ax**2 + ay**2)
        return f"|a| = √(x²+y²) = {sp.simplify(length)} ≈ {float(length):.4f}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def goc_giua_hai_vecto_tool(vecto_a: str, vecto_b: str) -> str:
    """Tính góc giữa hai vectơ dựa trên tích vô hướng và độ dài từng vectơ.

    Args:
        vecto_a: tọa độ vectơ a, dạng "x,y", ví dụ "1,0".
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
    so_gan_dung: float, so_dung: float = None, sai_so_tuyet_doi_da_biet: float = None,
) -> str:
    """Tính sai số tuyệt đối hoặc sai số tương đối của 1 số gần đúng.

    Args:
        operation: "tuyet_doi" (cần so_dung) hoặc "tuong_doi" (cần so_dung hoặc sai_so_tuyet_doi_da_biet).
        so_gan_dung: giá trị gần đúng.
        so_dung: giá trị đúng (nếu biết).
        sai_so_tuyet_doi_da_biet: sai số tuyệt đối đã biết trước (dùng khi không có so_dung).
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
    """Tính số trung bình (mean) của 1 mẫu số liệu.

    Args:
        so_lieu: các giá trị số liệu, cách nhau bởi dấu phẩy, ví dụ "2, 4, 6, 8, 10".
    """
    try:
        nums = _parse_numbers(so_lieu)
        mean = sum(nums) / len(nums)
        return f"Số trung bình = {sp.simplify(mean)} ≈ {float(mean):.4f}"
    except Exception as e:
        return f"LOI: {e}"


@tool
def tinh_trung_vi_mode_tool(so_lieu: str, operation: Literal["trung_vi", "mode"] = "trung_vi") -> str:
    """Tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.

    Args:
        so_lieu: các giá trị số liệu, cách nhau bởi dấu phẩy, ví dụ "1, 3, 3, 6, 7, 8, 9".
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
    """Tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.

    Args:
        so_lieu: các giá trị số liệu, cách nhau bởi dấu phẩy, ví dụ "2, 4, 6, 8, 10".
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