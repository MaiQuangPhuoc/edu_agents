from langchain_core.tools import tool
import sympy as sp


@tool
def check_point_in_region(a: float, b: float, c: float, x0: float, y0: float, sign: str = "<=") -> str:
    """Kiểm tra một điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn không.

    Dùng khi câu hỏi yêu cầu kiểm tra điểm có thuộc miền nghiệm của bất phương trình
    dạng ax + by <= c (hoặc >=, <, >) hay không.

    Args:
        a: hệ số của x.
        b: hệ số của y.
        c: hằng số vế phải.
        x0: hoành độ điểm cần kiểm tra.
        y0: tung độ điểm cần kiểm tra.
        sign: dấu bất phương trình, một trong "<=", ">=", "<", ">". Mặc định "<=".

    Returns:
        "True" nếu điểm thỏa mãn, "False" nếu không, hoặc "LOI:" nếu lỗi.
    """
    try:
        value = a * x0 + b * y0
        ops = {
            "<=": value <= c,
            ">=": value >= c,
            "<": value < c,
            ">": value > c,
        }
        if sign not in ops:
            return f"LOI: dau khong hop le - {sign}"
        return str(ops[sign])
    except Exception as e:
        return f"LOI: khong the kiem tra diem - {e}"


@tool
def linear_optimize(a: float, b: float, vertices: str, mode: str = "max") -> str:
    """Tìm giá trị lớn nhất hoặc nhỏ nhất của biểu thức F = ax + by trên miền đa giác.

    Dùng khi câu hỏi yêu cầu tìm GTLN hoặc GTNN của F = ax + by trên một miền nghiệm
    là đa giác, đã biết tọa độ các đỉnh của đa giác đó.

    Args:
        a: hệ số của x trong biểu thức F = ax + by.
        b: hệ số của y trong biểu thức F = ax + by.
        vertices: danh sách tọa độ đỉnh đa giác, dạng "x1,y1; x2,y2; x3,y3",
            ví dụ "0,0; 4,0; 2,3".
        mode: "max" để tìm GTLN, "min" để tìm GTNN. Mặc định "max".

    Returns:
        Chuỗi mô tả giá trị tối ưu và tọa độ đỉnh đạt được, hoặc "LOI:" nếu lỗi.
    """
    try:
        points = []
        for pair in vertices.split(";"):
            x_str, y_str = pair.strip().split(",")
            points.append((sp.sympify(x_str.strip()), sp.sympify(y_str.strip())))

        values = [(a * x + b * y, (x, y)) for x, y in points]

        if mode == "max":
            best = max(values, key=lambda v: float(v[0]))
        elif mode == "min":
            best = min(values, key=lambda v: float(v[0]))
        else:
            return f"LOI: mode khong hop le - {mode}"

        return f"F = {best[0]} tai diem ({best[1][0]}, {best[1][1]})"
    except Exception as e:
        return f"LOI: khong the toi uu - {e}"


INEQUALITY_TOOLS = [check_point_in_region, linear_optimize]