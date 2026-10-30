"""Two-sided one-sample and Welch two-sample t tests."""

import math
from collections.abc import Iterable
from dataclasses import dataclass

from ._common import mean, regularized_beta, sample


@dataclass(frozen=True)
class TestResult:
    """Test statistic, two-sided p-value, and degrees of freedom."""

    statistic: float
    p_value: float
    degrees_of_freedom: float


def _two_sided_t_p_value(statistic: float, degrees_of_freedom: float) -> float:
    x = degrees_of_freedom / (degrees_of_freedom + statistic * statistic)
    return regularized_beta(x, degrees_of_freedom / 2.0, 0.5)


def one_sample_t_test(values: Iterable[float], population_mean: float) -> TestResult:
    """Test the null that a sample's population mean equals ``population_mean``.

    Returns the t statistic, two-sided p-value, and ``n - 1`` degrees of
    freedom. At least two observations and nonzero sample variance are needed.
    """
    data = sample(values)
    if len(data) < 2:
        raise ValueError("at least two observations are required")
    try:
        target = float(population_mean)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("population_mean must be finite") from exc
    if not math.isfinite(target):
        raise ValueError("population_mean must be finite")
    center = mean(data)
    variance = math.fsum((value - center) ** 2 for value in data) / (len(data) - 1)
    if variance == 0:
        raise ValueError("t test requires non-zero sample variance")
    df = float(len(data) - 1)
    statistic = (center - target) / math.sqrt(variance / len(data))
    return TestResult(statistic, _two_sided_t_p_value(statistic, df), df)


def welch_t_test(first: Iterable[float], second: Iterable[float]) -> TestResult:
    """Welch's two-sided t test for equality of two independent means."""
    x, y = sample(first, "first"), sample(second, "second")
    if len(x) < 2 or len(y) < 2:
        raise ValueError("each sample must contain at least two observations")
    mx, my = mean(x), mean(y)
    vx = math.fsum((value - mx) ** 2 for value in x) / (len(x) - 1)
    vy = math.fsum((value - my) ** 2 for value in y) / (len(y) - 1)
    term_x, term_y = vx / len(x), vy / len(y)
    standard_error_squared = term_x + term_y
    if standard_error_squared == 0:
        raise ValueError("t test requires non-zero variation")
    df = standard_error_squared**2 / (
        term_x**2 / (len(x) - 1) + term_y**2 / (len(y) - 1)
    )
    statistic = (mx - my) / math.sqrt(standard_error_squared)
    return TestResult(statistic, _two_sided_t_p_value(statistic, df), df)
