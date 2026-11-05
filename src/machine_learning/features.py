"""Leakage-aware return feature construction."""

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureSet:
    """Feature rows, next-period targets, and column names."""

    features: tuple[tuple[float, ...], ...]
    targets: tuple[float, ...]
    feature_names: tuple[str, ...]


def build_return_features(
    prices: Iterable[float],
    lags: Sequence[int] = (1, 2, 3),
    volatility_windows: Sequence[int] = (5, 20),
) -> FeatureSet:
    """Build lagged simple returns and rolling volatility to predict next return.

    Each feature row uses returns through time ``t`` and its target is the
    return at ``t + 1``. Volatility uses sample standard deviation over each
    trailing window. Price history and window sizes must be valid and finite.
    """
    try:
        close = [float(value) for value in prices]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("prices must contain finite numeric values") from exc
    if len(close) < 3 or any(not math.isfinite(value) or value <= 0 for value in close):
        raise ValueError("prices must contain at least three positive finite values")
    lag_values = _validate_windows(lags, "lags", minimum=1)
    vol_windows = _validate_windows(volatility_windows, "volatility_windows", minimum=2)
    if not lag_values and not vol_windows:
        raise ValueError("at least one lag or volatility window is required")
    returns = [close[i] / close[i - 1] - 1.0 for i in range(1, len(close))]
    if any(not math.isfinite(value) for value in returns):
        raise ValueError("prices produce non-finite returns")
    first = max(
        max((lag - 1 for lag in lag_values), default=0),
        max((window - 1 for window in vol_windows), default=0),
    )
    if first + 1 >= len(returns):
        raise ValueError("not enough prices for requested windows and next-period targets")
    names = tuple(
        [f"return_lag_{lag}" for lag in lag_values]
        + [f"volatility_{window}" for window in vol_windows]
    )
    rows, targets = [], []
    for index in range(first, len(returns) - 1):
        row = [returns[index - lag + 1] for lag in lag_values]
        for window in vol_windows:
            sample = returns[index - window + 1 : index + 1]
            center = math.fsum(sample) / window
            row.append(math.sqrt(math.fsum((value - center) ** 2 for value in sample) / (window - 1)))
        rows.append(tuple(row))
        targets.append(returns[index + 1])
    return FeatureSet(tuple(rows), tuple(targets), names)


def _validate_windows(values: Sequence[int], name: str, minimum: int) -> tuple[int, ...]:
    try:
        result = tuple(values)
    except TypeError as exc:
        raise ValueError(f"{name} must be a sequence of positive integers") from exc
    if any(isinstance(value, bool) or not isinstance(value, int) or value < minimum for value in result):
        raise ValueError(f"{name} values must be integers >= {minimum}")
    if len(set(result)) != len(result):
        raise ValueError(f"{name} must not contain duplicates")
    return result
