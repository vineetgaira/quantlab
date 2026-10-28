import math

import pytest

from src.differential_equations import euler_method, runge_kutta_4


@pytest.mark.parametrize("method", [euler_method, runge_kutta_4])
def test_constant_derivative_is_integrated(method):
    times, values = method(lambda t, y: 2.0, 0.0, 1.0, 1.0, 0.25)
    assert times == pytest.approx([0, 0.25, 0.5, 0.75, 1.0])
    assert values == pytest.approx([1, 1.5, 2, 2.5, 3])


def test_euler_uses_forward_slope():
    times, values = euler_method(lambda t, y: y, 0, 1, 1, 0.25)
    assert times[-1] == 1
    assert values[-1] == pytest.approx((1 + 0.25) ** 4)


def test_runge_kutta_fourth_order_approximates_exponential():
    times, values = runge_kutta_4(lambda t, y: y, 0, 1, 1, 0.1)
    assert times[-1] == 1
    assert values[-1] == pytest.approx(math.e, abs=1e-5)


@pytest.mark.parametrize("method", [euler_method, runge_kutta_4])
def test_methods_short_final_step_and_integrate_backwards(method):
    times, values = method(lambda t, y: 1.0, 0, 0, 1, 0.3)
    assert times[-1] == 1
    assert values[-1] == pytest.approx(1)

    reverse_times, reverse_values = method(lambda t, y: 1.0, 1, 1, 0, 0.3)
    assert reverse_times[-1] == 0
    assert reverse_values[-1] == pytest.approx(0)


@pytest.mark.parametrize("method", [euler_method, runge_kutta_4])
def test_methods_zero_length_range_returns_initial_value(method):
    assert method(lambda t, y: y, 2, 3, 2, 0.1) == ([2.0], [3.0])


@pytest.mark.parametrize("method", [euler_method, runge_kutta_4])
def test_methods_reject_invalid_step_and_nonfinite_derivative(method):
    with pytest.raises(ValueError, match="positive step size"):
        method(lambda t, y: y, 0, 1, 1, 0)
    with pytest.raises(ValueError, match="finite numeric value"):
        method(lambda t, y: float("nan"), 0, 1, 1, 0.1)
