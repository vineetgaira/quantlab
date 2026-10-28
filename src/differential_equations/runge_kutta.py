"""Classical fourth-order Runge-Kutta initial-value solver."""

from collections.abc import Callable

from ._common import derivative, step_sizes, validate_inputs


def runge_kutta_4(
    f: Callable[[float, float], float],
    t0: float,
    y0: float,
    t_end: float,
    h: float,
) -> tuple[list[float], list[float]]:
    """Solve ``y' = f(t, y)`` using classical fourth-order Runge-Kutta.

    Returns the time and solution values, including both initial and final
    points. A shorter final step is used when ``h`` does not divide the range.
    """
    t0, y0, t_end, h = validate_inputs(f, t0, y0, t_end, h)
    times, values = [t0], [y0]
    t, y = t0, y0
    for dt in step_sizes(t0, t_end, h):
        k1 = derivative(f, t, y)
        k2 = derivative(f, t + dt / 2, y + dt * k1 / 2)
        k3 = derivative(f, t + dt / 2, y + dt * k2 / 2)
        k4 = derivative(f, t + dt, y + dt * k3)
        y += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += dt
        if t == t_end or abs(t - t_end) <= 1e-15 * max(1.0, abs(t_end)):
            t = t_end
        times.append(t)
        values.append(y)
    return times, values
