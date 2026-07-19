from langchain_core.tools import tool
import sympy as sp


def _parse_set(items: str) -> set:
    """Parse chuỗi số cách nhau bởi dấu phẩy thành set số thực."""
    return {sp.sympify(x.strip()) for x in items.split(",") if x.strip()}


@tool
def set_union(set_a: str, set_b: str) -> str:
    """Tính hợp của hai tập hợp số.

    Dùng khi câu hỏi yêu cầu tìm A ∪ B (hợp hai tập hợp).

    Args:
        set_a: các phần tử tập A, cách nhau bởi dấu phẩy, ví dụ "1, 2, 3".
        set_b: các phần tử tập B, cách nhau bởi dấu phẩy, ví dụ "2, 3, 4".

    Returns:
        Chuỗi liệt kê các phần tử của A ∪ B, hoặc "LOI:" nếu không xử lý được.
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        result = sorted(a | b, key=lambda x: float(x))
        return "{" + ", ".join(str(x) for x in result) + "}"
    except Exception as e:
        return f"LOI: khong the tinh hop - {e}"


@tool
def set_intersection(set_a: str, set_b: str) -> str:
    """Tính giao của hai tập hợp số.

    Dùng khi câu hỏi yêu cầu tìm A ∩ B (giao hai tập hợp).

    Args:
        set_a: các phần tử tập A, cách nhau bởi dấu phẩy.
        set_b: các phần tử tập B, cách nhau bởi dấu phẩy.

    Returns:
        Chuỗi liệt kê các phần tử của A ∩ B, hoặc "LOI:" nếu không xử lý được.
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        result = sorted(a & b, key=lambda x: float(x))
        return "{" + ", ".join(str(x) for x in result) + "}"
    except Exception as e:
        return f"LOI: khong the tinh giao - {e}"


@tool
def set_difference(set_a: str, set_b: str) -> str:
    """Tính hiệu của hai tập hợp số (A \\ B).

    Dùng khi câu hỏi yêu cầu tìm A \\ B (các phần tử thuộc A nhưng không thuộc B).

    Args:
        set_a: các phần tử tập A, cách nhau bởi dấu phẩy.
        set_b: các phần tử tập B, cách nhau bởi dấu phẩy.

    Returns:
        Chuỗi liệt kê các phần tử của A \\ B, hoặc "LOI:" nếu không xử lý được.
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        result = sorted(a - b, key=lambda x: float(x))
        return "{" + ", ".join(str(x) for x in result) + "}"
    except Exception as e:
        return f"LOI: khong the tinh hieu - {e}"


@tool
def is_subset(set_a: str, set_b: str) -> str:
    """Kiểm tra tập A có phải tập con của tập B không (A ⊂ B).

    Dùng khi câu hỏi yêu cầu kiểm tra quan hệ tập con giữa hai tập hợp.

    Args:
        set_a: các phần tử tập A, cách nhau bởi dấu phẩy.
        set_b: các phần tử tập B, cách nhau bởi dấu phẩy.

    Returns:
        "True" nếu A là tập con của B, "False" nếu không, hoặc "LOI:" nếu lỗi.
    """
    try:
        a, b = _parse_set(set_a), _parse_set(set_b)
        return str(a.issubset(b))
    except Exception as e:
        return f"LOI: khong the kiem tra tap con - {e}"


SET_TOOLS = [set_union, set_intersection, set_difference, is_subset]