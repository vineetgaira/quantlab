import math

import pytest

from src.simulation import analyze_distribution, simulate_gbm, simulate_gbm_paths


def test_gbm_path_shape_start_and_repeatability():
    first = simulate_gbm(100, 0.05, 0.2, 1, 12, seed=7)
    assert len(first) == 13
    assert first[0] == 100
    assert all(price > 0 and math.isfinite(price) for price in first)
    assert first == simulate_gbm(100, 0.05, 0.2, 1, 12, seed=7)


def test_zero_volatility_path_is_deterministic():
    path = simulate_gbm(100, 0.1, 0, 1, 4, seed=5)
    assert path[-1] == pytest.approx(100 * math.exp(0.1))


def test_multi_path_shape_and_reproducibility():
    paths = simulate_gbm_paths(50, 0.03, 0.25, 2, 8, 20, seed=42)
    assert len(paths) == 20
    assert all(len(path) == 9 and path[0] == 50 for path in paths)
    assert paths == simulate_gbm_paths(50, 0.03, 0.25, 2, 8, 20, seed=42)


@pytest.mark.parametrize(
    "args", [(0, 0.1, 0.2, 1, 10), (1, 0.1, -0.2, 1, 10), (1, 0.1, 0.2, -1, 10), (1, 0.1, 0.2, 1, 0)]
)
def test_gbm_rejects_invalid_parameters(args):
    with pytest.raises(ValueError):
        simulate_gbm(*args)


def test_multi_path_rejects_nonpositive_path_count():
    with pytest.raises(ValueError, match="n_paths"):
        simulate_gbm_paths(100, 0.05, 0.2, 1, 10, 0)


def test_distribution_summary_and_mean_confidence_interval():
    summary = analyze_distribution([1, 2, 3, 4, 5])
    assert summary.count == 5
    assert summary.mean == pytest.approx(3)
    assert summary.standard_deviation == pytest.approx(math.sqrt(2.5))
    assert summary.confidence_interval[0] < summary.mean < summary.confidence_interval[1]
    assert analyze_distribution([1, 2, 3], 0.9).confidence_level == 0.9


def test_distribution_analysis_validates_sample_and_confidence_level():
    with pytest.raises(ValueError):
        analyze_distribution([1])
    with pytest.raises(ValueError, match="confidence_level"):
        analyze_distribution([1, 2], 1)
