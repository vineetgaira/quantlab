"""LU decomposition with partial pivoting."""

from collections.abc import Sequence

from ._common import validate_system


def lu_decomposition(
    matrix: Sequence[Sequence[float]],
) -> tuple[list[list[float]], list[list[float]], list[list[float]]]:
    """Factor a square matrix as ``P @ A == L @ U``.

    Returns the permutation, unit lower-triangular, and upper-triangular
    matrices ``(P, L, U)``. Partial pivoting is used. Singular input raises
    ``ValueError``.
    """
    a, _ = validate_system(matrix, [0.0] * len(matrix))
    n = len(a)
    p = [[float(i == j) for j in range(n)] for i in range(n)]
    l = [[float(i == j) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if a[pivot][col] == 0:
            raise ValueError("matrix is singular")
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            p[col], p[pivot] = p[pivot], p[col]
            l[col][:col], l[pivot][:col] = l[pivot][:col], l[col][:col]
        for row in range(col + 1, n):
            factor = a[row][col] / a[col][col]
            l[row][col] = factor
            for j in range(col, n):
                a[row][j] -= factor * a[col][j]
    return p, l, a
