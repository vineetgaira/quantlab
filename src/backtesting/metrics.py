"""Annualized performance and drawdown measures for equity curves."""

import math
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class PerformanceMetrics:
    """Common annualized performance and risk measures."""

    cagr: float
    sharpe_ratio: float
    calmar_ratio: float
    volatility: float
    max_drawdown: float


def performance_metrics(
    equity_curve: Iterable[float],
    periods_per_year: int = 252,
    risk_free_rate: float = 0.0,
) -> PerformanceMetrics:
    """Compute CAGR, Sharpe, Calmar, annualized volatility, and max drawdown.

    Equity observations are assumed equally spaced. CAGR and annualization use
    ``periods_per_year``; Sharpe uses per-period returns and a per-period
    risk-free rate derived from the annual rate.
    """
    try:
        equity = [float(value) for value in equity_curve]
        risk_free_rate = float(risk_free_rate)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("equity and risk_free_rate must be finite numbers") from exc
    if len(equity) < 2 or any(not math.isfinite(value) or value <= 0 for value in equity):
        raise ValueError("equity_curve must contain at least two positive finite values")
    if isinstance(periods_per_year, bool) or not isinstance(periods_per_year, int) or periods_per_year < 1:
        raise ValueError("periods_per_year must be a positive integer")
    if not math.isfinite(risk_free_rate):
        raise ValueError("risk_free_rate must be finite")
    periods = len(equity) - 1
    years = periods / periods_per_year
    cagr = (equity[-1] / equity[0]) ** (1.0 / years) - 1.0
    returns = [equity[i] / equity[i - 1] - 1.0 for i in range(1, len(equity))]
    excess = [value - risk_free_rate / periods_per_year for value in returns]
    average = math.fsum(excess) / len(excess)
    variance = (
        math.fsum((value - average) ** 2 for value in excess) / (len(excess) - 1)
        if len(excess) > 1 else 0.0
    )
    volatility = math.sqrt(variance * periods_per_year)
    sharpe = average / math.sqrt(variance) * math.sqrt(periods_per_year) if variance else 0.0
    peak = equity[0]
    max_drawdown = 0.0
    for value in equity:
        peak = max(peak, value)
        max_drawdown = max(max_drawdown, (peak - value) / peak)
    calmar = cagr / max_drawdown if max_drawdown else 0.0
    return PerformanceMetrics(cagr, sharpe, calmar, volatility, max_drawdown)
