"""Cox-Ross-Rubinstein binomial tree for European options."""

import math

from .black_scholes import OptionType, _inputs


def crr_binomial_price(
    spot: float,
    strike: float,
    time_to_maturity: float,
    rate: float,
    volatility: float,
    steps: int = 100,
    option_type: OptionType = "call",
) -> float:
    """Price a European call or put using a CRR binomial tree.

    Assumes no dividends and continuously compounded rates. Raises ``ValueError``
    when the inputs imply a risk-neutral probability outside ``[0, 1]``.
    """
    s, k, t, r, sigma, kind = _inputs(
        spot, strike, time_to_maturity, rate, volatility, option_type
    )
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError("steps must be a positive integer")
    if t == 0:
        return max(s - k, 0.0) if kind == "call" else max(k - s, 0.0)
    dt = t / steps
    discount = math.exp(-r * dt)
    if sigma == 0:
        terminal_spot = s * math.exp(r * t)
        payoff = max(terminal_spot - k, 0.0) if kind == "call" else max(k - terminal_spot, 0.0)
        return math.exp(-r * t) * payoff
    up = math.exp(sigma * math.sqrt(dt))
    down = 1.0 / up
    probability = (math.exp(r * dt) - down) / (up - down)
    if not 0.0 <= probability <= 1.0:
        raise ValueError("risk-neutral probability is outside [0, 1]; adjust steps or inputs")
    values = []
    for up_moves in range(steps + 1):
        terminal_spot = s * up**up_moves * down ** (steps - up_moves)
        values.append(
            max(terminal_spot - k, 0.0)
            if kind == "call"
            else max(k - terminal_spot, 0.0)
        )
    for level in range(steps - 1, -1, -1):
        values = [
            discount * (probability * values[i + 1] + (1.0 - probability) * values[i])
            for i in range(level + 1)
        ]
    return values[0]
