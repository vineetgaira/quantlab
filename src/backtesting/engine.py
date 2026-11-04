"""Close-to-close backtesting engine with turnover costs and trade records."""

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from .metrics import PerformanceMetrics, performance_metrics
from .strategy import Strategy


@dataclass(frozen=True)
class TradeEvent:
    """A target exposure change and its estimated transaction cost."""

    index: int
    timestamp: Any
    price: float
    previous_exposure: float
    target_exposure: float
    turnover: float
    transaction_cost: float


@dataclass(frozen=True)
class Trade:
    """A completed continuous long or short position episode."""

    direction: str
    entry_index: int
    exit_index: int
    entry_timestamp: Any
    exit_timestamp: Any
    entry_price: float
    exit_price: float
    pnl: float
    return_on_entry_equity: float


@dataclass(frozen=True)
class BacktestResult:
    """Equity, exposure, event log, completed trades, and summary metrics."""

    equity_curve: tuple[float, ...]
    exposures: tuple[float, ...]
    events: tuple[TradeEvent, ...]
    trades: tuple[Trade, ...]
    metrics: PerformanceMetrics


@dataclass
class _OpenTrade:
    direction: str
    entry_index: int
    entry_timestamp: Any
    entry_price: float
    entry_equity: float
    pnl: float = 0.0


def run_backtest(
    prices: Sequence[float],
    strategy: Strategy,
    timestamps: Sequence[Any] | None = None,
    *,
    initial_capital: float = 10_000.0,
    transaction_cost: float = 0.0,
    periods_per_year: int = 252,
    risk_free_rate: float = 0.0,
) -> BacktestResult:
    """Run a strategy on close prices and return equity and trade analytics.

    The strategy observes the close at index ``i`` and its target exposure earns
    the return from close ``i`` to close ``i + 1``. Transaction cost is a
    fraction of equity per unit of absolute exposure change. The final open
    position is liquidated at the last close, including its exit cost.
    """
    if not isinstance(strategy, Strategy):
        raise ValueError("strategy must be an instance of Strategy")
    try:
        values = [float(price) for price in prices]
        capital, cost_rate = float(initial_capital), float(transaction_cost)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("prices, initial_capital, and transaction_cost must be finite") from exc
    if len(values) < 2 or any(not math.isfinite(value) or value <= 0 for value in values):
        raise ValueError("prices must contain at least two positive finite values")
    if not math.isfinite(capital) or capital <= 0:
        raise ValueError("initial_capital must be positive and finite")
    if not math.isfinite(cost_rate) or cost_rate < 0:
        raise ValueError("transaction_cost must be finite and non-negative")
    if timestamps is None:
        dates: list[Any] = list(range(len(values)))
    else:
        dates = list(timestamps)
        if len(dates) != len(values):
            raise ValueError("timestamps and prices must have the same length")

    equity = capital
    curve = [equity]
    exposures: list[float] = []
    events: list[TradeEvent] = []
    trades: list[Trade] = []
    current_exposure = 0.0
    active: _OpenTrade | None = None
    for index, price in enumerate(values):
        if index > 0:
            period_return = price / values[index - 1] - 1.0
            pnl = equity * current_exposure * period_return
            equity += pnl
            if active is not None:
                active.pnl += pnl
            if not math.isfinite(equity) or equity <= 0:
                raise RuntimeError("backtest equity became non-positive or non-finite")

        if index == len(values) - 1:
            target = 0.0  # Liquidate any open position at the final close.
        else:
            try:
                target = float(strategy.on_bar(index, price, values[: index + 1]))
            except (TypeError, ValueError, OverflowError) as exc:
                raise ValueError("strategy exposure must be a finite number") from exc
            if not math.isfinite(target):
                raise ValueError("strategy exposure must be a finite number")

        turnover = abs(target - current_exposure)
        fee = equity * turnover * cost_rate
        if turnover > 0:
            events.append(
                TradeEvent(index, dates[index], price, current_exposure, target, turnover, fee)
            )
            equity -= fee
            if active is not None:
                active.pnl -= fee
            old_direction = "long" if current_exposure > 0 else "short" if current_exposure < 0 else None
            new_direction = "long" if target > 0 else "short" if target < 0 else None
            if active is not None and (new_direction != old_direction or target == 0):
                trades.append(
                    Trade(
                        active.direction, active.entry_index, index,
                        active.entry_timestamp, dates[index], active.entry_price,
                        price, active.pnl, active.pnl / active.entry_equity,
                    )
                )
                active = None
            if active is None and target != 0:
                active = _OpenTrade(
                    new_direction or "long", index, dates[index], price, equity
                )
        current_exposure = target
        exposures.append(target)
        curve.append(equity)

    metrics = performance_metrics(curve, periods_per_year, risk_free_rate)
    return BacktestResult(tuple(curve), tuple(exposures), tuple(events), tuple(trades), metrics)
