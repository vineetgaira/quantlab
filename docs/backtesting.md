# Backtesting

The `src.backtesting` package provides a close-to-close strategy framework,
portfolio performance metrics, and execution and round-trip trade records.

```python
from src.backtesting import Strategy, run_backtest

class BuyAndHold(Strategy):
    def on_bar(self, index, price, history):
        return 1.0

result = run_backtest(prices, BuyAndHold(), transaction_cost=0.001)
print(result.metrics.cagr, result.metrics.sharpe_ratio)
print(result.trades)
```

## Strategy and timing

Subclass `Strategy` and implement `on_bar(index, price, history)`. Return a
finite target exposure: `1` is fully long, `0` is flat, and `-1` is fully short.
The callback sees prices only through the current close. Its target is applied
at that close and earns the next close-to-close return. The engine liquidates an
open position at the final close.

`run_backtest(prices, strategy, timestamps=None, initial_capital=10000,
transaction_cost=0, periods_per_year=252, risk_free_rate=0)` accepts positive
finite prices and optional labels for each observation. Transaction cost is a
fraction of current equity multiplied by the absolute exposure change, charged
when each target is applied. Leverage and short exposures are permitted when
returned by the strategy; the engine does not model margin, borrowing fees,
slippage, taxes, or market impact.

## Results and metrics

`BacktestResult` contains the equity curve, target exposures, `TradeEvent` log,
completed position episode `Trade` records, and a `PerformanceMetrics` value.
Trade P&L includes the strategy's price returns and transaction costs during
the episode. An execution event records the timestamp, price, old and new
exposure, turnover, and fee.

`performance_metrics(equity_curve, periods_per_year=252, risk_free_rate=0)`
returns CAGR, annualized Sharpe ratio, Calmar ratio, annualized volatility, and
maximum peak-to-trough drawdown. Observations are assumed equally spaced. The
Sharpe ratio uses sample standard deviation of per-period excess returns.
