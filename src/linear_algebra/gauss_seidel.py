"""Gauss-Seidel iteration for linear systems."""

from collections.abc import Sequence

from ._common import check_diagonal, validate_iteration_options, validate_system


def gauss_seidel_method(
    matrix: Sequence[Sequence[float]],
    vector: Sequence[float],
    initial_guess: Sequence[float] | None = None,
    tol: float = 1e-10,
    max_iter: int = 1000,
) -> list[float]:
    """Approximately solve ``A x = b`` by Gauss-Seidel iteration.

    Convergence is declared when the infinity norm of successive iterates is
    at most ``tol``. Raises ``RuntimeError`` if the iteration limit is reached.
    """
    a, b = validate_system(matrix, vector)
    check_diagonal(a)
    x, tol = validate_iteration_options(initial_guess, len(a), tol, max_iter)
    for _ in range(max_iter):
        previous = x.copy()
        for i in range(len(a)):
            x[i] = (b[i] - sum(a[i][j] * x[j] for j in range(len(a)) if j != i)) / a[i][i]
        if max(abs(x[i] - previous[i]) for i in range(len(a))) <= tol:
            return x
    raise RuntimeError("Gauss-Seidel method did not converge")
