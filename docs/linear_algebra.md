# Linear algebra

The `src.linear_algebra` package provides a direct solver, a matrix
factorization, and two iterative solvers for square systems `A x = b`. Inputs
may be sequences of numbers; matrices must be non-empty and square, and the
right-hand side must have the same dimension. Results are returned as Python
lists of floats. Invalid or non-finite values raise `ValueError`.

```python
from src.linear_algebra import (
    gauss_seidel_method,
    gaussian_elimination,
    jacobi_method,
    lu_decomposition,
)

A = [[4, 1], [2, 3]]
b = [1, 2]
print(gaussian_elimination(A, b))
print(jacobi_method(A, b))
print(gauss_seidel_method(A, b))
P, L, U = lu_decomposition(A)  # P @ A = L @ U
```

## Gaussian elimination

`gaussian_elimination(matrix, vector)` performs forward elimination with
partial pivoting, followed by back substitution. It raises `ValueError` if
the matrix is singular.

## LU decomposition

`lu_decomposition(matrix)` returns `(P, L, U)` such that `P @ A = L @ U`.
`P` is a permutation matrix, `L` is unit lower triangular, and `U` is upper
triangular. Partial pivoting is used. A singular matrix raises `ValueError`.

## Iterative methods

`jacobi_method(matrix, vector, initial_guess=None, tol=1e-10, max_iter=1000)`
and `gauss_seidel_method(...)` approximate the solution. The default initial
guess is the zero vector. Both stop when the infinity norm of the change
between successive iterates is at most `tol`; zero diagonal entries and
invalid options raise `ValueError`. If the stopping rule is not reached in
`max_iter` iterations, they raise `RuntimeError`. These stationary iterations
are not guaranteed to converge for every matrix; diagonal dominance is a
common sufficient condition.
