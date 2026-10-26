"""Newton-Raphson root-finding method."""

import math
from collections.abc import Callable

from ._common import evaluate, validate_options


def newton_raphson_method(
    f: Callable[[float], float],
    derivative: Callable[[float], float],
    x0: float,
    tol: float = 1e-5,
    max_iter: int = 100,
) -> float:
    """Find a root with Newton-Raphson iteration, starting from ``x0``."""
    validate_options(tol, max_iter)
    if not callable(derivative):
        raise ValueError("derivative must be callable")
    x = float(x0)
    if not math.isfinite(x):
        raise ValueError("x0 must be finite")
    for _ in range(max_iter):
        fx = evaluate(f, x)
        if abs(fx) <= tol:
            return x
        dfx = evaluate(derivative, x)
        if dfx == 0:
            raise ValueError("derivative is zero; Newton-Raphson cannot continue")
        next_x = x - fx / dfx
        if not math.isfinite(next_x):
            raise ValueError("iteration produced a non-finite value")
        if abs(next_x - x) <= tol:
            if abs(evaluate(f, next_x)) <= tol:
                return next_x
        x = next_x
    raise RuntimeError("Newton-Raphson method did not converge within max_iter")
