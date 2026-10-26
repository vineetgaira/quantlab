import math

import pytest

from src.roots import (
    bisection_method,
    false_position_method,
    newton_raphson_method,
    secant_method,
)


@pytest.mark.parametrize(
    "method, args",
    [
        (bisection_method, (0.0, 2.0)),
        (false_position_method, (0.0, 2.0)),
        (newton_raphson_method, (None, 1.0)),
        (secant_method, (1.0, 2.0)),
    ],
)
def test_methods_find_sqrt_two(method, args):
    f = lambda x: x * x - 2
    if method is newton_raphson_method:
        root = method(f, lambda x: 2 * x, args[1], tol=1e-10)
    else:
        root = method(f, *args, tol=1e-10)
    assert root == pytest.approx(math.sqrt(2), abs=1e-9)


@pytest.mark.parametrize("method", [bisection_method, false_position_method])
def test_bracketed_methods_return_endpoint_root(method):
    assert method(lambda x: x, 0.0, 2.0) == 0.0


def test_bracketed_methods_reject_interval_without_sign_change():
    for method in (bisection_method, false_position_method):
        with pytest.raises(ValueError, match="opposite signs"):
            method(lambda x: x * x + 1, -1.0, 1.0)


def test_newton_raphson_rejects_zero_derivative():
    with pytest.raises(ValueError, match="derivative is zero"):
        newton_raphson_method(lambda x: x + 1, lambda x: 0, 0.0)


def test_secant_rejects_equal_function_values():
    with pytest.raises(ValueError, match="function values are equal"):
        secant_method(lambda x: x * x + 1, -1.0, 1.0)


def test_methods_validate_tolerance_and_report_non_convergence():
    with pytest.raises(ValueError, match="tol"):
        bisection_method(lambda x: x, -1.0, 1.0, tol=0)
    with pytest.raises(RuntimeError, match="did not converge"):
        bisection_method(lambda x: x * x - 2, 0.0, 2.0, tol=1e-15, max_iter=1)


def test_newton_raphson_returns_initial_estimate_when_it_is_a_root():
    assert newton_raphson_method(lambda x: x * x, lambda x: 2 * x, 0.0) == 0.0
