import pytest

from src.statistics import (
    correlation,
    covariance,
    mean,
    median,
    mode,
    one_sample_t_test,
    simple_linear_regression,
    standard_deviation,
    variance,
    welch_t_test,
)


def test_descriptive_statistics():
    assert mean([1, 2, 3, 4]) == pytest.approx(2.5)
    assert median([1, 4, 2, 3]) == pytest.approx(2.5)
    assert mode([1, 2, 2, 3, 3]) == [2.0, 3.0]
    assert mode([1, 2, 3]) == []
    assert variance([1, 2, 3]) == pytest.approx(1.0)
    assert variance([1, 2, 3], sample_variance=False) == pytest.approx(2 / 3)
    assert standard_deviation([1, 2, 3]) == pytest.approx(1.0)


def test_covariance_and_correlation():
    assert covariance([1, 2, 3], [2, 4, 6]) == pytest.approx(2.0)
    assert covariance([1, 2, 3], [2, 4, 6], sample_covariance=False) == pytest.approx(4 / 3)
    assert correlation([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)
    assert correlation([1, 2, 3], [6, 4, 2]) == pytest.approx(-1.0)
    with pytest.raises(ValueError, match="constant"):
        correlation([1, 1], [2, 3])


def test_simple_linear_regression():
    fit = simple_linear_regression([1, 2, 3], [3, 5, 7])
    assert fit.slope == pytest.approx(2.0)
    assert fit.intercept == pytest.approx(1.0)
    assert fit.r_squared == pytest.approx(1.0)
    assert fit.predict(4) == pytest.approx(9.0)


def test_one_sample_t_test_matches_known_result():
    result = one_sample_t_test([2, 4, 6], population_mean=0)
    assert result.statistic == pytest.approx(3.4641016151)
    assert result.degrees_of_freedom == 2
    assert result.p_value == pytest.approx(0.0741799002, rel=1e-7)


def test_welch_t_test_detects_difference():
    result = welch_t_test([1, 2, 3, 4], [8, 9, 10, 11])
    assert result.statistic < 0
    assert result.p_value < 0.01
    assert result.degrees_of_freedom > 0


def test_statistics_validate_data():
    for function in (mean, median, mode, variance):
        with pytest.raises(ValueError):
            function([])
    with pytest.raises(ValueError, match="same length"):
        covariance([1, 2], [1])
    with pytest.raises(ValueError, match="distinct x"):
        simple_linear_regression([1, 1], [2, 3])
    with pytest.raises(ValueError, match="non-zero sample variance"):
        one_sample_t_test([2, 2], 1)
