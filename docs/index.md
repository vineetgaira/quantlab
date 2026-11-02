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

## Running the tests

From the repository root, run:

```bash
pytest
```
