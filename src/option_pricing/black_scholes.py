"""Black-Scholes European option pricing and Greeks."""

import math
from typing import Literal

OptionType = Literal["call", "put"]


def _inputs(
    spot: float, strike: float, time_to_maturity: float, rate: float, volatility: float,
    option_type: str,
) -> tuple[float, float, float, float, float, OptionType]:
    try:
        spot, strike, maturity, rate, volatility = map(
            float, (spot, strike, time_to_maturity, rate, volatility)
        )
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("option parameters must be finite numbers") from exc
    if not all(math.isfinite(v) for v in (spot, strike, maturity, rate, volatility)):
        raise ValueError("option parameters must be finite numbers")
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")
    if maturity < 0 or volatility < 0:
        raise ValueError("time_to_maturity and volatility must be non-negative")
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'")
    return spot, strike, maturity, rate, volatility, option_type  # type: ignore[return-value]


def _cdf(value: float) -> float:
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def _pdf(value: float) -> float:
    return math.exp(-0.5 * value * value) / math.sqrt(2.0 * math.pi)


def _d1_d2(spot: float, strike: float, maturity: float, rate: float, volatility: float):
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility**2) * maturity) / (
        volatility * math.sqrt(maturity)
    )
    return d1, d1 - volatility * math.sqrt(maturity)


def black_scholes_price(
    spot: float,
    strike: float,
    time_to_maturity: float,
    rate: float,
    volatility: float,
    option_type: OptionType = "call",
) -> float:
    """Return the Black-Scholes value of a European call or put.

    The model assumes no dividends and continuously compounded risk-free rate.
    ``time_to_maturity`` is in years and ``volatility`` is annualized.
    """
    s, k, t, r, sigma, kind = _inputs(
        spot, strike, time_to_maturity, rate, volatility, option_type
    )
    discount = math.exp(-r * t)
    if t == 0:
        return max(s - k, 0.0) if kind == "call" else max(k - s, 0.0)
    if sigma == 0:
        forward_spot = s * math.exp(r * t)
        payoff = max(forward_spot - k, 0.0) if kind == "call" else max(k - forward_spot, 0.0)
        return discount * payoff
    d1, d2 = _d1_d2(s, k, t, r, sigma)
    if kind == "call":
        return s * _cdf(d1) - k * discount * _cdf(d2)
    return k * discount * _cdf(-d2) - s * _cdf(-d1)


def black_scholes_greeks(
    spot: float,
    strike: float,
    time_to_maturity: float,
    rate: float,
    volatility: float,
    option_type: OptionType = "call",
) -> dict[str, float]:
    """Return ``delta``, ``gamma``, ``vega``, and annual ``theta``.

    Vega is the price change for a 1.00 change in annual volatility (so a
    one-percentage-point change is approximately ``0.01 * vega``).
    """
    s, k, t, r, sigma, kind = _inputs(
        spot, strike, time_to_maturity, rate, volatility, option_type
    )
    if t == 0:
        delta = 1.0 if s > k else 0.0 if s < k else 0.5
        if kind == "put":
            delta -= 1.0
        return {"delta": delta, "gamma": 0.0, "vega": 0.0, "theta": 0.0}
    if sigma == 0:
        forward_spot = s * math.exp(r * t)
        if kind == "call":
            delta = 1.0 if forward_spot > k else 0.0
            theta = -r * k * math.exp(-r * t) if delta else 0.0
        else:
            delta = -1.0 if forward_spot < k else 0.0
            theta = r * k * math.exp(-r * t) if delta else 0.0
        return {"delta": delta, "gamma": 0.0, "vega": 0.0, "theta": theta}
    d1, d2 = _d1_d2(s, k, t, r, sigma)
    density = _pdf(d1)
    gamma = density / (s * sigma * math.sqrt(t))
    vega = s * density * math.sqrt(t)
    common = -s * density * sigma / (2.0 * math.sqrt(t))
    if kind == "call":
        delta = _cdf(d1)
        theta = common - r * k * math.exp(-r * t) * _cdf(d2)
    else:
        delta = _cdf(d1) - 1.0
        theta = common + r * k * math.exp(-r * t) * _cdf(-d2)
    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta}
