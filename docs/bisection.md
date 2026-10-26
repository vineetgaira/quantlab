# Bisection method

`bisection_method` finds a zero of a continuous scalar function inside an
interval whose endpoint values have opposite signs (or one endpoint is already
a zero). It repeatedly halves the interval and keeps the half that still
brackets a sign change.

```python
from src.roots import bisection_method

root = bisection_method(lambda x: x * x - 2, 0.0, 2.0, tol=1e-10)
print(root)  # approximately 1.4142135624
```

## Interface

```python
bisection_method(f, a, b, tol=1e-5, max_iter=100)
```

- `f`: callable that returns a finite numeric value for each evaluated input.
- `a`, `b`: finite endpoints with `a < b`.
- `tol`: finite positive tolerance. The method stops when the absolute
  function value or half the current interval width is at most this value.
- `max_iter`: positive integer limiting the number of bisection steps.
- Returns: the approximate root as a `float`.

The method raises `ValueError` for invalid options, a malformed interval, or
non-finite function values. An interval without a sign change is rejected. It
raises `RuntimeError` if the iteration limit is reached before convergence.
An endpoint that is exactly a root is returned immediately.

## Guarantees and limitations

For a continuous function with a valid bracket, bisection maintains a bracket
containing at least one root. It converges reliably, but only finds a root in
the supplied interval and does not identify which root when several are
bracketed. The tolerance applies to the residual or half-width stopping rule;
it is not a promise of relative error in the returned root.
