"""Descriptive summaries and confidence intervals for simulated values."""

import math
from collections.abc import Iterable
from dataclasses import dataclass
from statistics import NormalDist


@dataclass(frozen=True)
class DistributionSummary:
    """Summary statistics and a confidence interval for the population mean."""

    count: int
    mean: float
    standard_deviation: float
    standard_error: float
    confidence_level: float
    confidence_interval: tuple[float, float]


def analyze_distribution(
    values: Iterable[float], confidence_level: float = 0.95
) -> DistributionSummary:
    """Summarize values and estimate a normal confidence interval for their mean.

    The interval uses the sample standard error and a two-sided normal critical
    value. At least two finite observations are required.
    """
    try:
        data = [float(value) for value in values]
        level = float(confidence_level)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("values and confidence_level must be finite numbers") from exc
    if len(data) < 2 or not all(math.isfinite(value) for value in data):
        raise ValueError("at least two finite observations are required")
    if not math.isfinite(level) or not 0 < level < 1:
        raise ValueError("confidence_level must be between 0 and 1")
    center = math.fsum(data) / len(data)
    variance = math.fsum((value - center) ** 2 for value in data) / (len(data) - 1)
    std = math.sqrt(variance)
    standard_error = std / math.sqrt(len(data))
    critical = NormalDist().inv_cdf((1 + level) / 2)
    margin = critical * standard_error
    return DistributionSummary(
        len(data), center, std, standard_error, level,
        (center - margin, center + margin),
    )
