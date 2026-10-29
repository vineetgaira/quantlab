"""Shared input validation for linear algebra algorithms."""

import math
from collections.abc import Sequence


def validate_system(
    matrix: Sequence[Sequence[float]], vector: Sequence[float]
) -> tuple[list[list[float]], list[float]]:
    """Convert and validate a square matrix and a compatible vector."""
    try:
        rows = [list(row) for row in matrix]
        rhs = list(vector)
    except (TypeError, ValueError) as exc:
        raise ValueError("matrix and vector must be finite numeric sequences") from exc
    if not rows or any(len(row) != len(rows) for row in rows):
        raise ValueError("matrix must be a non-empty square matrix")
    if len(rhs) != len(rows):
        raise ValueError("vector length must match matrix dimensions")
    try:
        rows = [[float(value) for value in row] for row in rows]
        rhs = [float(value) for value in rhs]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("matrix and vector must contain finite numbers") from exc
    if not all(math.isfinite(value) for row in rows for value in row) or not all(
        math.isfinite(value) for value in rhs
    ):
        raise ValueError("matrix and vector must contain finite numbers")
    return rows, rhs


def validate_iteration_options(
    initial_guess: Sequence[float] | None, size: int, tol: float, max_iter: int
) -> tuple[list[float], float]:
    try:
        tol = float(tol)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("tol must be a finite positive number") from exc
    if not math.isfinite(tol) or tol <= 0:
        raise ValueError("tol must be a finite positive number")
    if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")
    if initial_guess is None:
        guess = [0.0] * size
    else:
        try:
            guess = [float(value) for value in initial_guess]
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("initial_guess must contain finite numbers") from exc
        if len(guess) != size or not all(math.isfinite(value) for value in guess):
            raise ValueError("initial_guess must contain one finite value per variable")
    return guess, tol


def check_diagonal(matrix: list[list[float]]) -> None:
    if any(matrix[i][i] == 0 for i in range(len(matrix))):
        raise ValueError("matrix diagonal entries must be non-zero")
