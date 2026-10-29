import pytest

from src.linear_algebra import (
    gauss_seidel_method,
    gaussian_elimination,
    jacobi_method,
    lu_decomposition,
)


MATRIX = [[4, 1], [2, 3]]
VECTOR = [1, 2]


def test_gaussian_elimination_solves_system_with_pivoting():
    assert gaussian_elimination([[0, 2], [1, 1]], [4, 3]) == pytest.approx([1, 2])


def test_gaussian_elimination_rejects_singular_matrix():
    with pytest.raises(ValueError, match="singular"):
        gaussian_elimination([[1, 2], [2, 4]], [3, 6])


def test_lu_decomposition_satisfies_p_a_equals_l_u():
    p, l, u = lu_decomposition([[0, 2], [1, 1]])
    for i in range(2):
        for j in range(2):
            assert sum(p[i][k] * [[0, 2], [1, 1]][k][j] for k in range(2)) == pytest.approx(
                sum(l[i][k] * u[k][j] for k in range(2))
            )


@pytest.mark.parametrize("method", [jacobi_method, gauss_seidel_method])
def test_iterative_methods_solve_diagonally_dominant_system(method):
    result = method([[4, 1], [2, 3]], [1, 2], tol=1e-12)
    assert result == pytest.approx([0.1, 0.6], abs=1e-10)


@pytest.mark.parametrize("method", [jacobi_method, gauss_seidel_method])
def test_iterative_methods_validate_diagonal_and_convergence(method):
    with pytest.raises(ValueError, match="diagonal"):
        method([[0, 1], [1, 2]], [1, 2])
    with pytest.raises(RuntimeError, match="did not converge"):
        method([[4, 1], [2, 3]], [1, 2], max_iter=1, tol=1e-15)


def test_linear_methods_validate_system_dimensions():
    with pytest.raises(ValueError, match="square"):
        gaussian_elimination([[1, 2]], [1])
    with pytest.raises(ValueError, match="length"):
        jacobi_method(MATRIX, [1])
