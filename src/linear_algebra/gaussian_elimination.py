"""Gaussian elimination with partial pivoting."""

from collections.abc import Sequence

from ._common import validate_system


def gaussian_elimination(
    matrix: Sequence[Sequence[float]], vector: Sequence[float]
) -> list[float]:
    """Solve ``A x = b`` using forward elimination and back substitution.

    Partial pivoting is used to reduce numerical error. A singular matrix raises
    ``ValueError``.
    """
    a, b = validate_system(matrix, vector)
    n = len(a)
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if a[pivot][col] == 0:
            raise ValueError("matrix is singular")
        a[col], a[pivot] = a[pivot], a[col]
        b[col], b[pivot] = b[pivot], b[col]
        for row in range(col + 1, n):
            factor = a[row][col] / a[col][col]
            a[row][col] = 0.0
            for j in range(col + 1, n):
                a[row][j] -= factor * a[col][j]
            b[row] -= factor * b[col]
    solution = [0.0] * n
    for row in range(n - 1, -1, -1):
        solution[row] = (b[row] - sum(a[row][j] * solution[j] for j in range(row + 1, n))) / a[row][row]
    return solution
