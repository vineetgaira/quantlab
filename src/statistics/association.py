"""Covariance and Pearson correlation for paired observations."""

import math
from collections.abc import Iterable

from ._common import mean, paired_samples


def covariance(
    x: Iterable[float], y: Iterable[float], *, sample_covariance: bool = True
) -> float:
    """Return sample covariance by default, or population covariance."""
    x_values, y_values = paired_samples(x, y)
    denominator = len(x_values) - 1 if sample_covariance else len(x_values)
    return math.fsum(
        (a - mean(x_values)) * (b - mean(y_values))
        for a, b in zip(x_values, y_values)
    ) / denominator


def correlation(x: Iterable[float], y: Iterable[float]) -> float:
    """Return Pearson's correlation coefficient; constant inputs are rejected."""
    x_values, y_values = paired_samples(x, y)
    x_center, y_center = mean(x_values), mean(y_values)
    x_ss = math.fsum((value - x_center) ** 2 for value in x_values)
    y_ss = math.fsum((value - y_center) ** 2 for value in y_values)
    if x_ss == 0 or y_ss == 0:
        raise ValueError("correlation is undefined for a constant sample")
    cross = math.fsum(
        (a - x_center) * (b - y_center) for a, b in zip(x_values, y_values)
    )
    return cross / math.sqrt(x_ss * y_ss)
