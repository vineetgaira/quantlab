"""Portfolio return and risk analytics."""

import math
from collections.abc import Sequence
from dataclasses import dataclass

from .core import portfolio_variance, validate_asset_inputs, validate_weights


@dataclass(frozen=True)
class PortfolioMetrics:
    """Portfolio weights and annualized return/risk measures."""

    weights: tuple[float, ...]
    expected_return: float
    volatility: float
    sharpe_ratio: float


def portfolio_performance(
    weights: Sequence[float],
    expected_returns: Sequence[float],
    covariance: Sequence[Sequence[float]],
    risk_free_rate: float = 0.0,
) -> PortfolioMetrics:
    """Compute weighted expected return, standard deviation, and Sharpe ratio."""
    returns, cov = validate_asset_inputs(expected_returns, covariance)
    w = validate_weights(weights, len(returns))
    try:
        risk_free_rate = float(risk_free_rate)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("risk_free_rate must be finite") from exc
    if not math.isfinite(risk_free_rate):
        raise ValueError("risk_free_rate must be finite")
    expected = sum(weight * value for weight, value in zip(w, returns))
    variance = portfolio_variance(w, cov)
    if variance < -1e-12:
        raise ValueError("covariance produces a negative portfolio variance")
    volatility = math.sqrt(max(variance, 0.0))
    sharpe = (expected - risk_free_rate) / volatility if volatility > 0 else 0.0
    return PortfolioMetrics(tuple(w), expected, volatility, sharpe)
