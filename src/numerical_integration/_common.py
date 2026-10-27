"""Shared validation for numerical integration methods."""

import math
from collections.abc import Callable


def validate_inputs(
    f: Callable[[float], float], a: float, b: float, n: int
) -> tuple[float, float]:
    if not callable(f):
        raise ValueError("f must be callable")
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("a and b must be finite numbers") from exc
    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("a and b must be finite numbers")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    return a, b


def evaluate(f: Callable[[float], float], x: float) -> float:
    try:
        value = float(f(x))
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("f must return a finite numeric value") from exc
    if not math.isfinite(value):
        raise ValueError("f must return a finite numeric value")
    return value
