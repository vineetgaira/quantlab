"""Descriptive and inferential statistical algorithms."""

from .association import correlation, covariance
from .descriptive import mean, median, mode, standard_deviation, variance
from .hypothesis import TestResult, one_sample_t_test, welch_t_test
from .regression import LinearRegressionResult, simple_linear_regression

__all__ = [
    "mean", "median", "mode", "variance", "standard_deviation",
    "covariance", "correlation", "LinearRegressionResult",
    "simple_linear_regression", "TestResult", "one_sample_t_test", "welch_t_test",
]
