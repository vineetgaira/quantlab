# Monte Carlo simulation

The `src.simulation` package generates geometric Brownian motion price paths
and summarizes simulated samples with confidence intervals. The implementation
uses Python's standard library and accepts an optional seed for reproducible
simulations.

```python
from src.simulation import analyze_distribution, simulate_gbm_paths

paths = simulate_gbm_paths(
    initial_price=100, drift=0.05, volatility=0.2,
    time_horizon=1, steps=252, n_paths=1000, seed=17,
)
terminal_prices = [path[-1] for path in paths]
summary = analyze_distribution(terminal_prices)
print(summary.mean, summary.confidence_interval)
```

## Geometric Brownian motion

`simulate_gbm(initial_price, drift, volatility, time_horizon, steps, seed=None)`
returns one path with `steps + 1` prices, including the starting price.
`simulate_gbm_paths(..., n_paths, seed=None)` returns a list of independent
paths of the same form. Drift and volatility are annualized; time horizon is
in years. Each step uses the exact GBM transition

`S(t + dt) = S(t) exp((drift - volatility²/2) dt + volatility sqrt(dt) Z)`

where `Z` is a standard normal random variable. The initial price must be
positive, volatility and horizon non-negative, and step and path counts positive
integers.

## Distribution analysis

`analyze_distribution(values, confidence_level=0.95)` returns a
`DistributionSummary` with `count`, `mean`, sample `standard_deviation`,
`standard_error`, the selected confidence level, and a two-sided normal
confidence interval for the population mean. At least two finite values are
required. This interval uses a normal critical value and is an approximation;
it may be unreliable for small samples from strongly non-normal distributions.
