"""Geometric Brownian motion path generation."""

import math
import random


def _validate_parameters(
    initial_price: float, drift: float, volatility: float, time_horizon: float, steps: int
) -> tuple[float, float, float, float]:
    try:
        initial_price, drift, volatility, time_horizon = map(
            float, (initial_price, drift, volatility, time_horizon)
        )
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("GBM parameters must be finite numbers") from exc
    if not all(math.isfinite(v) for v in (initial_price, drift, volatility, time_horizon)):
        raise ValueError("GBM parameters must be finite numbers")
    if initial_price <= 0:
        raise ValueError("initial_price must be positive")
    if volatility < 0:
        raise ValueError("volatility must be non-negative")
    if time_horizon < 0:
        raise ValueError("time_horizon must be non-negative")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError("steps must be a positive integer")
    return initial_price, drift, volatility, time_horizon


def simulate_gbm(
    initial_price: float,
    drift: float,
    volatility: float,
    time_horizon: float,
    steps: int,
    *,
    seed: int | None = None,
) -> list[float]:
    """Generate one exact-step GBM path, including the initial price.

    ``drift`` and ``volatility`` are annualized and ``time_horizon`` is in
    years. The returned list has ``steps + 1`` prices. Supplying ``seed`` makes
    the path reproducible.
    """
    s0, mu, sigma, horizon = _validate_parameters(
        initial_price, drift, volatility, time_horizon, steps
    )
    dt = horizon / steps
    rng = random.Random(seed)
    prices = [s0]
    price = s0
    for _ in range(steps):
        z = rng.gauss(0.0, 1.0)
        price *= math.exp((mu - 0.5 * sigma * sigma) * dt + sigma * math.sqrt(dt) * z)
        prices.append(price)
    return prices


def simulate_gbm_paths(
    initial_price: float,
    drift: float,
    volatility: float,
    time_horizon: float,
    steps: int,
    n_paths: int,
    *,
    seed: int | None = None,
) -> list[list[float]]:
    """Generate ``n_paths`` independent GBM paths as lists of prices."""
    _validate_parameters(initial_price, drift, volatility, time_horizon, steps)
    if isinstance(n_paths, bool) or not isinstance(n_paths, int) or n_paths < 1:
        raise ValueError("n_paths must be a positive integer")
    rng = random.Random(seed)
    paths = []
    for _ in range(n_paths):
        path_seed = rng.getrandbits(64)
        paths.append(
            simulate_gbm(
                initial_price,
                drift,
                volatility,
                time_horizon,
                steps,
                seed=path_seed,
            )
        )
    return paths
