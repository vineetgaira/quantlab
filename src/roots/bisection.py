"""Bisection root-finding method."""

from collections.abc import Callable

from ._common import evaluate, validate_bracket, validate_options


def bisection_method(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-5,
    max_iter: int = 100,
) -> float:
    """Find a root in a sign-changing interval using bisection.

    Stop when the residual or the bracket width is at most ``tol``. Raises
    ``ValueError`` for invalid inputs and ``RuntimeError`` if iteration ends
    before convergence.
    """
    validate_options(tol, max_iter)
    fa, fb = validate_bracket(f, a, b)
    if fa == 0:
        return float(a)
    if fb == 0:
        return float(b)

    for _ in range(max_iter):
        midpoint = a + (b - a) / 2
        fm = evaluate(f, midpoint)
        if abs(fm) <= tol or (b - a) / 2 <= tol:
            return midpoint
        if (fa > 0) == (fm > 0):
            a, fa = midpoint, fm
        else:
            b, fb = midpoint, fm
    raise RuntimeError("bisection method did not converge within max_iter")
