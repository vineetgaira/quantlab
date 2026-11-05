# QuantLab documentation

QuantLab currently provides scalar root-finding methods implemented in Python.
The package is available from `src.roots`.

## Root finding

- [Bisection method](bisection.md)

The root-finding module also includes false position, Newton–Raphson, and secant
methods. Their public functions are exported by `src.roots`.

## Numerical integration

- [Numerical integration methods](numerical_integration.md)

## Differential equations

- [Ordinary differential equation solvers](differential_equations.md)

## Linear algebra

- [Linear system solvers and matrix factorization](linear_algebra.md)

## Statistics

- [Descriptive and inferential statistics](statistics.md)

## Monte Carlo simulation

- [Geometric Brownian motion and distribution analysis](simulation.md)

## Option pricing

- [Black-Scholes, Greeks, and CRR binomial pricing](option_pricing.md)

## Portfolio optimization

- [Mean-variance portfolio construction and analytics](portfolio_optimization.md)

## Backtesting

- [Strategy simulation and performance metrics](backtesting.md)

## Machine learning

- [Time-series features, prediction, volatility, and regimes](machine_learning.md)

## Running the tests

From the repository root, run:

```bash
pytest
```
