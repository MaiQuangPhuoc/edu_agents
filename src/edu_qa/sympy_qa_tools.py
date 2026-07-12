import sympy as sp


def _to_expr(expression: str):
    x, y = sp.symbols("x y")
    return sp.sympify(expression, locals={"x": x, "y": y})


def sympy_diff(expression: str, variable: str = "x") -> dict:
    try:
        var = sp.symbols(variable)
        expr = _to_expr(expression)
        result = sp.diff(expr, var)
        return {"status": "ok", "result": str(sp.simplify(result))}
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def sympy_solve(expression: str, variable: str = "x") -> dict:
    try:
        var = sp.symbols(variable)
        expr = _to_expr(expression)
        result = sp.solve(sp.Eq(expr, 0) if "=" not in expression else expr, var)
        return {"status": "ok", "result": [str(r) for r in result]}
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def sympy_simplify(expression: str) -> dict:
    try:
        expr = _to_expr(expression)
        result = sp.simplify(expr)
        return {"status": "ok", "result": str(result)}
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def sympy_evaluate(expression: str) -> dict:
    try:
        expr = _to_expr(expression)
        result = sp.N(expr)
        return {"status": "ok", "result": str(result)}
    except Exception as e:
        return {"status": "error", "reason": str(e)}


TOOL_MAP = {
    "diff":     sympy_diff,
    "solve":    sympy_solve,
    "simplify": sympy_simplify,
    "evaluate": sympy_evaluate,
}


def run_tool(operation: str, expression: str, variable: str = "x") -> dict:
    fn = TOOL_MAP.get(operation)
    if not fn:
        return {"status": "error", "reason": f"Không hỗ trợ operation: {operation}"}
    if operation in ("diff", "solve"):
        return fn(expression, variable)
    return fn(expression)