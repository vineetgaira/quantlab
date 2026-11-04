"""Strategy backtesting and trade-level performance analysis."""

from .engine import BacktestResult, Trade, TradeEvent, run_backtest
from .metrics import PerformanceMetrics, performance_metrics
from .strategy import Strategy

__all__ = [
    "BacktestResult",
    "PerformanceMetrics",
    "Strategy",
    "Trade",
    "TradeEvent",
    "performance_metrics",
    "run_backtest",
]
