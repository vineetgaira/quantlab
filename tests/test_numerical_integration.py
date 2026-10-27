import pytest

from src.numerical_integration import (
    simpsons_one_third,
    simpsons_three_eighths,
    trapezoidal_rule,
)


@pytest.mark.parametrize(
    "method,n",
    [
        (trapezoidal_rule, 1000),
        (simpsons_one_third, 10),
        (simpsons_three_eighths, 12),
    ],
)
def test_methods_integrate_constant(method, n):
    assert method(lambda x: 3.0, 0, 2, n) == pytest.approx(6.0)


def test_trapezoidal_rule_integrates_linear_function_exactly():
    assert trapezoidal_rule(lambda x: 2 * x + 1, -1, 3, 4) == pytest.approx(12.0)


def test_simpsons_one_third_integrates_cubic_exactly():
    assert simpsons_one_third(lambda x: x**3, 0, 2, 4) == pytest.approx(4.0)


def test_simpsons_three_eighths_integrates_cubic_exactly():
    assert simpsons_three_eighths(lambda x: x**3, 0, 2, 6) == pytest.approx(4.0)


@pytest.mark.parametrize(
    "method,n,match",
    [
        (simpsons_one_third, 3, "even"),
        (simpsons_three_eighths, 4, "divisible by 3"),
    ],
)
def test_simpson_methods_require_valid_subinterval_counts(method, n, match):
    with pytest.raises(ValueError, match=match):
        method(lambda x: x, 0, 1, n)


@pytest.mark.parametrize("method", [trapezoidal_rule, simpsons_one_third, simpsons_three_eighths])
def test_methods_support_reversed_and_equal_limits(method):
    forward = method(lambda x: x * x, 0, 1, 6)
    reverse = method(lambda x: x * x, 1, 0, 6)
    assert reverse == pytest.approx(-forward)
    assert method(lambda x: x * x, 2, 2, 6) == 0.0


@pytest.mark.parametrize("method", [trapezoidal_rule, simpsons_one_third, simpsons_three_eighths])
def test_methods_validate_interval_count_and_integrand(method):
    with pytest.raises(ValueError, match="positive integer"):
        method(lambda x: x, 0, 1, 0)
    with pytest.raises(ValueError, match="finite"):
        method(lambda x: float("nan"), 0, 1, 6)
    with pytest.raises(ValueError, match="finite"):
        method(lambda x: x, 0, float("inf"), 6)
