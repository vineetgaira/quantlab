"""Input validation and small numerical helpers for statistics."""

import math
from collections.abc import Iterable


def sample(values: Iterable[float], name: str = "values") -> list[float]:
    try:
        result = [float(value) for value in values]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must contain finite numeric values") from exc
    if not result or not all(math.isfinite(value) for value in result):
        raise ValueError(f"{name} must contain finite numeric values")
    return result


def paired_samples(x: Iterable[float], y: Iterable[float]) -> tuple[list[float], list[float]]:
    x_values, y_values = sample(x, "x"), sample(y, "y")
    if len(x_values) != len(y_values):
        raise ValueError("x and y must have the same length")
    if len(x_values) < 2:
        raise ValueError("at least two paired observations are required")
    return x_values, y_values


def mean(values: list[float]) -> float:
    return math.fsum(values) / len(values)


def regularized_beta(x: float, a: float, b: float) -> float:
    """Regularized incomplete beta via a continued fraction (Numerical Recipes)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0

    def fraction(aa: float, bb: float, xx: float) -> float:
        qab, qap, qam = aa + bb, aa + 1.0, aa - 1.0
        c, d = 1.0, 1.0 - qab * xx / qap
        tiny = 1e-300
        if abs(d) < tiny:
            d = tiny
        d = 1.0 / d
        h = d
        for m in range(1, 201):
            m2 = 2 * m
            term = m * (bb - m) * xx / ((qam + m2) * (aa + m2))
            d = 1.0 + term * d
            if abs(d) < tiny:
                d = tiny
            c = 1.0 + term / c
            if abs(c) < tiny:
                c = tiny
            d = 1.0 / d
            h *= d * c
            term = -(aa + m) * (qab + m) * xx / ((aa + m2) * (qap + m2))
            d = 1.0 + term * d
            if abs(d) < tiny:
                d = tiny
            c = 1.0 + term / c
            if abs(c) < tiny:
                c = tiny
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < 3e-14:
                break
        return h

    front = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log1p(-x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return front * fraction(a, b, x) / a
    return 1.0 - front * fraction(b, a, 1.0 - x) / b
