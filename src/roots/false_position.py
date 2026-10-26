"""False-position (Regula Falsi) root-finding method."""

from collections.abc import Callable

from ._common import evaluate, validate_bracket, validate_options


def false_position_method(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-5,
    max_iter: int = 100,
) -> float:
    """Find a bracketed root using the false-position method."""
    validate_options(tol, max_iter)
    fa, fb = validate_bracket(f, a, b)
    if fa == 0:
        return float(a)
    if fb == 0:
        return float(b)
    for _ in range(max_iter):
        denominator = fb - fa
        if denominator == 0:
            raise ValueError(
                "function values are equal; false-position cannot continue"
            )
        x = (a * fb - b * fa) / denominator
        fx = evaluate(f, x)
        if abs(fx) <= tol:
            return x
        if (fa > 0) == (fx > 0):
            a, fa = x, fx
        else:
            b, fb = x, fx
    raise RuntimeError("false-position method did not converge within max_iter")
