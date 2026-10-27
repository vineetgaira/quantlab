# Numerical integration

The `src.numerical_integration` package implements three composite rules for
approximating definite integrals. Each method divides the interval into equal
subintervals and evaluates a scalar function at the resulting points.

```python
from src.numerical_integration import (
    simpsons_one_third,
    simpsons_three_eighths,
    trapezoidal_rule,
)

f = lambda x: x**2
print(trapezoidal_rule(f, 0, 1, n=100))
print(simpsons_one_third(f, 0, 1, n=10))
print(simpsons_three_eighths(f, 0, 1, n=12))
```

Each function has the form `method(f, a, b, n=...)`. `f` must be callable and
return finite numeric values; `a` and `b` must be finite numbers. `n` is the
positive integer number of subintervals. The result is a float. Reversing the
limits changes the sign, and equal limits return zero. Invalid arguments,
non-finite limits, or non-finite function results raise `ValueError`.

## Composite trapezoidal rule

`trapezoidal_rule(f, a, b, n=100)` approximates the area under each interval
with a trapezoid. It accepts any positive `n`. For smooth functions, its global
error is generally second order in the subinterval width.

## Composite Simpson's 1/3 rule

`simpsons_one_third(f, a, b, n=100)` applies quadratic interpolation over pairs
of subintervals. `n` must be even. It is exact, up to floating-point rounding,
for polynomials of degree at most three and generally has fourth-order global
error for sufficiently smooth functions.

## Composite Simpson's 3/8 rule

`simpsons_three_eighths(f, a, b, n=99)` applies cubic interpolation in groups
of three subintervals. `n` must be divisible by three. It is exact, up to
floating-point rounding, for polynomials of degree at most three and generally
has fourth-order global error for sufficiently smooth functions.

The Simpson rules reject a subinterval count that does not meet their parity
or divisibility requirement. These methods assume a well-behaved integrand on
the interval; they do not detect discontinuities or singularities in the
interior.
