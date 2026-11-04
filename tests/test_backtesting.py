import pytest

from src.backtesting import Strategy, performance_metrics, run_backtest


class BuyAndHold(Strategy):
    def on_bar(self, index, price, history):
        return 1.0


class ThresholdStrategy(Strategy):
    def on_bar(self, index, price, history):
        return 1.0 if price < 105 else 0.0


def test_backtest_buy_and_hold_tracks_returns_and_closes_final_trade():
    result = run_backtest([100, 110, 99], BuyAndHold(), initial_capital=1000)
    assert result.equity_curve == pytest.approx([1000, 1000, 1100, 990])
    assert result.exposures == (1.0, 1.0, 0.0)
    assert len(result.trades) == 1
    assert result.trades[0].direction == "long"
    assert result.trades[0].pnl == pytest.approx(-10)


def test_strategy_receives_history_and_execution_costs_are_logged():
    result = run_backtest(
        [100, 101, 106, 103], ThresholdStrategy(), transaction_cost=0.01,
        timestamps=["a", "b", "c", "d"],
    )
    assert len(result.events) == 2
    assert result.events[0].timestamp == "a"
    assert result.events[0].turnover == 1
    assert result.events[0].transaction_cost == pytest.approx(100)
    assert len(result.trades) == 1
    assert result.trades[0].exit_timestamp == "c"


def test_performance_metrics_calculate_drawdown_and_annualized_values():
    result = performance_metrics([100, 110, 99, 108], periods_per_year=3)
    assert result.max_drawdown == pytest.approx(0.1)
    assert result.cagr == pytest.approx((108 / 100) ** (3 / 3) - 1)
    assert result.volatility > 0
    assert result.sharpe_ratio > 0


def test_backtest_validates_inputs_and_strategy_exposure():
    with pytest.raises(ValueError, match="at least two"):
        run_backtest([100], BuyAndHold())
    with pytest.raises(ValueError, match="same length"):
        run_backtest([100, 101], BuyAndHold(), timestamps=["only one"])

    class InvalidExposure(Strategy):
        def on_bar(self, index, price, history):
            return float("nan")

    with pytest.raises(ValueError, match="finite"):
        run_backtest([100, 101], InvalidExposure())


def test_metric_input_validation():
    with pytest.raises(ValueError, match="positive finite"):
        performance_metrics([100, 0])
