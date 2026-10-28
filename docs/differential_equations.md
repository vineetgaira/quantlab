# Ordinary differential equation solvers

The `src.differential_equations` package solves scalar initial-value problems
of the form `dy/dt = f(t, y)`, with `y(t0) = y0`.

```python
from src.differential_equations import euler_method, runge_kutta_4

f = lambda t, y: y
times, euler_values = euler_method(f, 0.0, 1.0, 1.0, 0.1)
times, rk4_values = runge_kutta_4(f, 0.0, 1.0, 1.0, 0.1)
```

Both functions accept `method(f, t0, y0, t_end, h)` and return a pair of lists:
the time points and the corresponding approximate solution values. The initial
point is included. The final point is included as well; if `h` does not evenly
divide the integration range, the final step is shortened. A positive `h` is
used in either direction, so `t_end` may be less than `t0`. When both endpoints
are equal, the result contains only the initial point.

The function `f` must be callable and return a finite numeric derivative at
each point. The initial values and step size must be finite, and `h` must be
positive. Invalid inputs or non-finite derivative results raise `ValueError`.

## Euler method

`euler_method` advances with the slope at the start of each step:

```text
y[n+1] = y[n] + h * f(t[n], y[n])
```

It is a first-order method: for a sufficiently smooth solution, the global
error typically decreases in proportion to the step size. It is simple and
fast, but may require a small step for useful accuracy or stability.

## Classical fourth-order Runge-Kutta

`runge_kutta_4` estimates the slope at the start, two midpoints, and the end of
each step, then combines those slopes with weights `1, 2, 2, 1`. It has
fourth-order global accuracy for sufficiently smooth solutions and is a useful
general-purpose fixed-step method. Neither solver estimates its own error or
automatically chooses a step size.
