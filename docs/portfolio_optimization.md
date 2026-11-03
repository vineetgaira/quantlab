# Portfolio optimization

The `src.portfolio_optimization` package implements long-only, fully invested
mean-variance portfolio tools. Expected returns and covariance must use
consistent periods and asset ordering. Weights are constrained to be
non-negative and sum to one. The package uses Python only and has no optimizer
dependency.

```python
from src.portfolio_optimization import (
    asset_covariance_matrix, efficient_frontier,
    maximum_sharpe_portfolio, minimum_variance_portfolio,
)

# observations are time rows by asset columns
cov = asset_covariance_matrix(historical_returns)
expected_returns = [0.08, 0.12, 0.10]
minimum = minimum_variance_portfolio(expected_returns, cov)
best_sharpe = maximum_sharpe_portfolio(expected_returns, cov, risk_free_rate=0.02)
frontier = efficient_frontier(expected_returns, cov, points=25)
```

## Covariance estimation

`asset_covariance_matrix(observations, sample_covariance=True)` computes
pairwise covariance from rows of observations. It uses denominator `n - 1` by
default and `n` when `sample_covariance=False`.

## Portfolio analytics

`portfolio_performance(weights, expected_returns, covariance, risk_free_rate=0)`
returns a `PortfolioMetrics` value containing weights, weighted expected
return, volatility, and Sharpe ratio. The inputs should be annualized (or share
another consistent period). A zero-volatility portfolio receives Sharpe ratio
zero.

## Optimization methods

`minimum_variance_portfolio(...)` uses projected gradient descent on portfolio
variance over the long-only simplex. `maximum_sharpe_portfolio(...)` uses
projected gradient ascent with backtracking line search from several starting
portfolios; it is a numerical solution to a non-convex objective.

`efficient_frontier(..., points=20)` minimizes variance at evenly spaced target
returns from the minimum to maximum asset expected return. It returns a list of
`PortfolioMetrics`. Each target solve projects onto the intersection of the
long-only simplex and the target-return hyperplane. These numerical methods
have finite iteration limits and can be sensitive to ill-conditioned or
non-positive-semidefinite covariance inputs; inspect results and model inputs
when applying them to real data.
