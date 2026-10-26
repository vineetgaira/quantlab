"""Shared validation helpers for scalar root-finding methods."""

import math
from collections.abc import Callable


def validate_options(tol: float, max_iter: int) -> None:
    if not math.isfinite(tol) or tol <= 0:
        raise ValueError("tol must be a finite positive number")
    if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")


def evaluate(f: Callable[[float], float], x: float) -> float:
    value = float(f(x))
    if not math.isfinite(value):
        raise ValueError("function must return a finite value")
    return value


def validate_bracket(
    f: Callable[[float], float], a: float, b: float
) -> tuple[float, float]:
    if not math.isfinite(a) or not math.isfinite(b) or a >= b:
        raise ValueError("a and b must be finite and satisfy a < b")
    fa, fb = evaluate(f, a), evaluate(f, b)
    if fa != 0 and fb != 0 and (fa > 0) == (fb > 0):
        raise ValueError("f(a) and f(b) must have opposite signs")
    return fa, fb
