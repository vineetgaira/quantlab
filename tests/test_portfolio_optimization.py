import pytest

from src.portfolio_optimization import (
    asset_covariance_matrix,
    efficient_frontier,
    maximum_sharpe_portfolio,
    minimum_variance_portfolio,
    portfolio_performance,
)


def test_asset_covariance_matrix_sample_and_population():
    observations = [[1, 2], [2, 4], [3, 6]]
    sample_cov = asset_covariance_matrix(observations)
    population_cov = asset_covariance_matrix(observations, sample_covariance=False)
    assert sample_cov[0] == pytest.approx([1, 2])
    assert sample_cov[1] == pytest.approx([2, 4])
    assert population_cov[0] == pytest.approx([2 / 3, 4 / 3])
    assert population_cov[1] == pytest.approx([4 / 3, 8 / 3])


RETURNS = [0.08, 0.12]
COVARIANCE = [[0.04, 0.006], [0.006, 0.09]]


def test_portfolio_performance():
    result = portfolio_performance([0.5, 0.5], RETURNS, COVARIANCE, 0.02)
    assert result.expected_return == pytest.approx(0.10)
    assert result.volatility == pytest.approx((0.04 + 0.006 + 0.006 + 0.09) ** 0.5 / 2)
    assert result.sharpe_ratio == pytest.approx(0.08 / result.volatility)


def test_minimum_variance_portfolio_is_fully_invested_and_low_risk():
    result = minimum_variance_portfolio(RETURNS, COVARIANCE)
    assert sum(result.weights) == pytest.approx(1.0)
    assert all(weight >= 0 for weight in result.weights)
    assert result.volatility < portfolio_performance([0.5, 0.5], RETURNS, COVARIANCE).volatility


def test_maximum_sharpe_portfolio_is_at_least_as_good_as_each_asset():
    result = maximum_sharpe_portfolio(RETURNS, COVARIANCE, risk_free_rate=0.02)
    assert sum(result.weights) == pytest.approx(1.0)
    asset_sharpes = [
        portfolio_performance([1, 0], RETURNS, COVARIANCE, 0.02).sharpe_ratio,
        portfolio_performance([0, 1], RETURNS, COVARIANCE, 0.02).sharpe_ratio,
    ]
    assert result.sharpe_ratio >= max(asset_sharpes) - 1e-8


def test_efficient_frontier_hits_return_range_and_is_ordered():
    points = efficient_frontier(RETURNS, COVARIANCE, points=5)
    assert len(points) == 5
    assert points[0].expected_return == pytest.approx(min(RETURNS), abs=1e-7)
    assert points[-1].expected_return == pytest.approx(max(RETURNS), abs=1e-7)
    assert [point.expected_return for point in points] == sorted(
        point.expected_return for point in points
    )
    assert all(sum(point.weights) == pytest.approx(1.0) for point in points)


def test_portfolio_inputs_are_validated():
    with pytest.raises(ValueError, match="at least two rows"):
        asset_covariance_matrix([[1, 2]])
    with pytest.raises(ValueError, match="symmetric"):
        portfolio_performance([0.5, 0.5], RETURNS, [[1, 0], [1, 1]])
    with pytest.raises(ValueError, match="sum to 1"):
        portfolio_performance([0.2, 0.2], RETURNS, COVARIANCE)
    with pytest.raises(ValueError, match="points"):
        efficient_frontier(RETURNS, COVARIANCE, points=1)
