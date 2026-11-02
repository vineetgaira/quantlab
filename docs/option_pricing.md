# Option pricing

The `src.option_pricing` package implements Black-Scholes European option
pricing, its principal Greeks, and a Cox-Ross-Rubinstein (CRR) binomial tree.
Both models assume no dividends, European exercise, and continuously
compounded risk-free rates.

```python
from src.option_pricing import (
    black_scholes_greeks, black_scholes_price, crr_binomial_price,
)

price = black_scholes_price(100, 100, 1, 0.05, 0.2, "call")
greeks = black_scholes_greeks(100, 100, 1, 0.05, 0.2, "call")
tree_price = crr_binomial_price(100, 100, 1, 0.05, 0.2, steps=500)
```

All three functions take spot, strike, time to maturity in years, continuously
compounded rate, and annualized volatility. Option type is `"call"` or `"put"`
and defaults to `"call"`. Spot and strike must be positive; maturity and
volatility must be non-negative. Invalid inputs raise `ValueError`.

## Black-Scholes price and Greeks

`black_scholes_price(...)` returns the European option value. The formula uses
the standard normal cumulative distribution function and handles zero maturity
and zero volatility directly.

`black_scholes_greeks(...)` returns a dictionary containing `delta`, `gamma`,
`vega`, and annual `theta`. Vega is per 1.00 change in volatility, so a one
percentage-point volatility change corresponds approximately to `0.01 * vega`.
At expiry, the implementation returns intrinsic-value delta (0.5 at the strike)
and zero for gamma, vega, and theta.

## CRR binomial tree

`crr_binomial_price(..., steps=100, option_type="call")` rolls European
terminal payoffs backward through a recombining tree. The CRR up and down
multipliers are `exp(volatility * sqrt(dt))` and its reciprocal. A risk-neutral
probability outside `[0, 1]` indicates the chosen step size and inputs are
incompatible and raises `ValueError`. The tree is recomputed in linear memory.
