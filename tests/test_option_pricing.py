import pytest

from src.option_pricing import (
    black_scholes_greeks,
    black_scholes_price,
    crr_binomial_price,
)


def test_black_scholes_prices_call_and_put_and_put_call_parity():
    call = black_scholes_price(100, 100, 1, 0.05, 0.2)
    put = black_scholes_price(100, 100, 1, 0.05, 0.2, "put")
    assert call == pytest.approx(10.45058357, abs=1e-7)
    assert put == pytest.approx(5.57352602, abs=1e-7)
    assert call - put == pytest.approx(100 - 100 * 2.718281828459045 ** -0.05)


def test_black_scholes_greeks_are_known_for_at_the_money_call():
    greeks = black_scholes_greeks(100, 100, 1, 0.05, 0.2)
    assert greeks["delta"] == pytest.approx(0.63683065, abs=1e-7)
    assert greeks["gamma"] == pytest.approx(0.01876202, abs=1e-7)
    assert greeks["vega"] == pytest.approx(37.52403469, abs=1e-7)
    assert greeks["theta"] == pytest.approx(-6.41402755, abs=1e-7)
    put_greeks = black_scholes_greeks(100, 100, 1, 0.05, 0.2, "put")
    assert put_greeks["delta"] == pytest.approx(-0.36316935, abs=1e-7)


def test_expired_and_zero_volatility_options():
    assert black_scholes_price(110, 100, 0, 0.05, 0.2) == 10
    assert black_scholes_price(100, 100, 1, 0.05, 0, "call") == pytest.approx(
        100 - 100 * 2.718281828459045 ** -0.05
    )


def test_crr_converges_toward_black_scholes():
    exact = black_scholes_price(100, 100, 1, 0.05, 0.2)
    tree = crr_binomial_price(100, 100, 1, 0.05, 0.2, steps=500)
    assert tree == pytest.approx(exact, abs=0.02)


def test_crr_prices_put_and_handles_expiry():
    assert crr_binomial_price(100, 100, 1, 0.05, 0.2, 400, "put") == pytest.approx(
        black_scholes_price(100, 100, 1, 0.05, 0.2, "put"), abs=0.03
    )
    assert crr_binomial_price(90, 100, 0, 0.05, 0.2) == 0


@pytest.mark.parametrize(
    "function,args",
    [
        (black_scholes_price, (0, 100, 1, 0.05, 0.2)),
        (black_scholes_price, (100, 100, 1, 0.05, 0.2, "digital")),
        (black_scholes_greeks, (100, 100, 1, 0.05, -0.2)),
        (crr_binomial_price, (100, 100, 1, 0.05, 0.2, 0)),
    ],
)
def test_pricers_reject_invalid_parameters(function, args):
    with pytest.raises(ValueError):
        function(*args)
