"""Long-only minimum-variance, maximum-Sharpe, and frontier algorithms."""

import math
from collections.abc import Sequence

from .analytics import PortfolioMetrics, portfolio_performance
from .core import (
    portfolio_variance,
    project_simplex,
    project_target,
    validate_asset_inputs,
)


def _spectral_step(covariance: list[list[float]]) -> float:
    bound = max(sum(abs(value) for value in row) for row in covariance)
    return 1.0 / max(2.0 * bound, 1e-12)


def _min_variance(
    covariance: list[list[float]],
    initial: Sequence[float] | None = None,
    expected_returns: Sequence[float] | None = None,
    target_return: float | None = None,
    max_iter: int = 20_000,
    tolerance: float = 1e-11,
) -> list[float]:
    n = len(covariance)
    weights = project_simplex(initial if initial is not None else [1.0 / n] * n)
    step = _spectral_step(covariance)
    for _ in range(max_iter):
        gradient = [2.0 * sum(covariance[i][j] * weights[j] for j in range(n)) for i in range(n)]
        candidate = [weights[i] - step * gradient[i] for i in range(n)]
        if target_return is None:
            updated = project_simplex(candidate)
        else:
            assert expected_returns is not None
            updated = project_target(candidate, expected_returns, target_return)
        if max(abs(updated[i] - weights[i]) for i in range(n)) <= tolerance:
            return updated
        weights = updated
    return weights


def minimum_variance_portfolio(
    expected_returns: Sequence[float],
    covariance: Sequence[Sequence[float]],
    risk_free_rate: float = 0.0,
) -> PortfolioMetrics:
    """Find the global minimum-variance long-only fully invested portfolio."""
    returns, cov = validate_asset_inputs(expected_returns, covariance)
    weights = _min_variance(cov)
    return portfolio_performance(weights, returns, cov, risk_free_rate)


def maximum_sharpe_portfolio(
    expected_returns: Sequence[float],
    covariance: Sequence[Sequence[float]],
    risk_free_rate: float = 0.0,
    max_iter: int = 20_000,
    tolerance: float = 1e-10,
) -> PortfolioMetrics:
    """Maximize the long-only Sharpe ratio by projected gradient ascent.

    Several deterministic starting points are considered to improve robustness
    of the non-convex ratio objective.
    """
    returns, cov = validate_asset_inputs(expected_returns, covariance)
    try:
        rf = float(risk_free_rate)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("risk_free_rate must be finite") from exc
    if not math.isfinite(rf):
        raise ValueError("risk_free_rate must be finite")
    n = len(returns)
    starts = [[1.0 / n] * n] + [[float(i == j) for i in range(n)] for j in range(n)]
    candidates: list[PortfolioMetrics] = []
    for weights in starts:
        score = portfolio_performance(weights, returns, cov, rf).sharpe_ratio
        for _ in range(max_iter):
            excess = sum(weights[i] * (returns[i] - rf) for i in range(n))
            variance = max(portfolio_variance(weights, cov), 1e-24)
            sigma = math.sqrt(variance)
            cov_w = [sum(cov[i][j] * weights[j] for j in range(n)) for i in range(n)]
            gradient = [
                (returns[i] - rf) / sigma - excess * cov_w[i] / (variance * sigma)
                for i in range(n)
            ]
            step = 1.0
            updated = weights
            updated_score = score
            while step > 1e-12:
                trial = project_simplex([weights[i] + step * gradient[i] for i in range(n)])
                trial_score = portfolio_performance(trial, returns, cov, rf).sharpe_ratio
                if trial_score >= score + 1e-4 * sum(
                    (trial[i] - weights[i]) * gradient[i] for i in range(n)
                ):
                    updated, updated_score = trial, trial_score
                    break
                step *= 0.5
            if max(abs(updated[i] - weights[i]) for i in range(n)) <= tolerance:
                break
            weights, score = updated, updated_score
        candidates.append(portfolio_performance(weights, returns, cov, rf))
    return max(candidates, key=lambda result: result.sharpe_ratio)


def efficient_frontier(
    expected_returns: Sequence[float],
    covariance: Sequence[Sequence[float]],
    points: int = 20,
    risk_free_rate: float = 0.0,
) -> list[PortfolioMetrics]:
    """Sample the long-only mean-variance frontier at evenly spaced targets.

    Each point minimizes variance subject to full investment, non-negative
    weights, and the target expected return. Target returns span the minimum
    through maximum individual expected returns.
    """
    returns, cov = validate_asset_inputs(expected_returns, covariance)
    if isinstance(points, bool) or not isinstance(points, int) or points < 2:
        raise ValueError("points must be an integer of at least 2")
    low, high = min(returns), max(returns)
    targets = [low + (high - low) * i / (points - 1) for i in range(points)]
    frontier = []
    for target in targets:
        weights = _min_variance(
            cov,
            initial=[1.0 / len(returns)] * len(returns),
            expected_returns=returns,
            target_return=target,
        )
        frontier.append(portfolio_performance(weights, returns, cov, risk_free_rate))
    return frontier
