"""Composite Simpson integration methods."""

import math
from collections.abc import Callable

from ._common import evaluate, validate_inputs


def simpsons_one_third(
    f: Callable[[float], float], a: float, b: float, n: int = 100
) -> float:
    """Approximate an integral with composite Simpson's 1/3 rule.

    ``n`` is the number of equal-width subintervals and must be even.
    """
    a, b = validate_inputs(f, a, b, n)
    if n % 2:
        raise ValueError("n must be even for Simpson's 1/3 rule")
    if a == b:
        return 0.0
    h = (b - a) / n
    weighted_sum = math.fsum(
        evaluate(f, a + i * h) * (1 if i in (0, n) else 4 if i % 2 else 2)
        for i in range(n + 1)
    )
    return h * weighted_sum / 3


def simpsons_three_eighths(
    f: Callable[[float], float], a: float, b: float, n: int = 99
) -> float:
    """Approximate an integral with composite Simpson's 3/8 rule.

    ``n`` is the number of equal-width subintervals and must be divisible by 3.
    """
    a, b = validate_inputs(f, a, b, n)
    if n % 3:
        raise ValueError("n must be divisible by 3 for Simpson's 3/8 rule")
    if a == b:
        return 0.0
    h = (b - a) / n
    weighted_sum = math.fsum(
        evaluate(f, a + i * h) * (1 if i in (0, n) else 2 if i % 3 == 0 else 3)
        for i in range(n + 1)
    )
    return 3 * h * weighted_sum / 8
