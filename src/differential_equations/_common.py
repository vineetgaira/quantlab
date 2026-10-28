"""Shared input validation and stepping helpers for ODE solvers."""

import math
from collections.abc import Callable


def validate_inputs(
    f: Callable[[float, float], float], t0: float, y0: float, t_end: float, h: float
) -> tuple[float, float, float, float]:
    if not callable(f):
        raise ValueError("f must be callable")
    try:
        t0, y0, t_end, h = float(t0), float(y0), float(t_end), float(h)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("t0, y0, t_end, and h must be finite numbers") from exc
    if not all(math.isfinite(value) for value in (t0, y0, t_end, h)):
        raise ValueError("t0, y0, t_end, and h must be finite numbers")
    if h <= 0:
        raise ValueError("h must be a finite positive step size")
    return t0, y0, t_end, h


def derivative(f: Callable[[float, float], float], t: float, y: float) -> float:
    try:
        value = float(f(t, y))
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("f must return a finite numeric value") from exc
    if not math.isfinite(value):
        raise ValueError("f must return a finite numeric value")
    return value


def step_sizes(t0: float, t_end: float, h: float) -> list[float]:
    """Return signed steps, shortening the final one to land on ``t_end``."""
    distance = abs(t_end - t0)
    if distance == 0:
        return []
    direction = 1.0 if t_end > t0 else -1.0
    full_steps = int(distance // h)
    steps = [direction * h] * full_steps
    remainder = distance - full_steps * h
    if remainder > 0:
        steps.append(direction * remainder)
    return steps
