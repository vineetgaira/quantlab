"""Composite trapezoidal integration."""

import math
from collections.abc import Callable

from ._common import evaluate, validate_inputs


def trapezoidal_rule(
    f: Callable[[float], float], a: float, b: float, n: int = 100
) -> float:
    """Approximate the definite integral of ``f`` from ``a`` to ``b``.

    ``n`` is the number of equal-width subintervals. Reversing the limits
    reverses the sign of the result.
    """
    a, b = validate_inputs(f, a, b, n)
    if a == b:
        return 0.0
    h = (b - a) / n
    weighted_sum = math.fsum(
        evaluate(f, a + i * h) * (0.5 if i in (0, n) else 1.0)
        for i in range(n + 1)
    )
    return h * weighted_sum
