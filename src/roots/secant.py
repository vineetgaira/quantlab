"""Secant root-finding method."""

import math
from collections.abc import Callable

from ._common import evaluate, validate_options


def secant_method(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float = 1e-5,
    max_iter: int = 100,
) -> float:
    """Find a root using the secant method from two initial estimates."""
    validate_options(tol, max_iter)
    x0, x1 = float(x0), float(x1)
    if not math.isfinite(x0) or not math.isfinite(x1):
        raise ValueError("initial estimates must be finite")
    f0, f1 = evaluate(f, x0), evaluate(f, x1)
    if abs(f0) <= tol:
        return x0
    if abs(f1) <= tol:
        return x1
    for _ in range(max_iter):
        denominator = f1 - f0
        if denominator == 0:
            raise ValueError(
                "function values are equal; secant iteration cannot continue"
            )
        x2 = x1 - f1 * (x1 - x0) / denominator
        if not math.isfinite(x2):
            raise ValueError("iteration produced a non-finite value")
        f2 = evaluate(f, x2)
        if abs(f2) <= tol or abs(x2 - x1) <= tol:
            if abs(f2) <= tol:
                return x2
        x0, f0, x1, f1 = x1, f1, x2, f2
    raise RuntimeError("secant method did not converge within max_iter")
