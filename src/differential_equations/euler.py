"""Forward Euler initial-value solver."""

from collections.abc import Callable

from ._common import derivative, step_sizes, validate_inputs


def euler_method(
    f: Callable[[float, float], float],
    t0: float,
    y0: float,
    t_end: float,
    h: float,
) -> tuple[list[float], list[float]]:
    """Solve ``y' = f(t, y)`` from ``t0`` to ``t_end`` with forward Euler.

    Returns the time and solution values, including both initial and final
    points. A shorter final step is used when ``h`` does not divide the range.
    """
    t0, y0, t_end, h = validate_inputs(f, t0, y0, t_end, h)
    times, values = [t0], [y0]
    t, y = t0, y0
    for dt in step_sizes(t0, t_end, h):
        y += dt * derivative(f, t, y)
        t += dt
        if t == t_end or abs(t - t_end) <= 1e-15 * max(1.0, abs(t_end)):
            t = t_end
        times.append(t)
        values.append(y)
    return times, values
