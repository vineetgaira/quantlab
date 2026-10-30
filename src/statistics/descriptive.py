"""Descriptive statistics for one-dimensional samples."""

import math
from collections import Counter
from collections.abc import Iterable

from ._common import mean as _mean
from ._common import sample


def mean(values: Iterable[float]) -> float:
    """Return the arithmetic mean."""
    return _mean(sample(values))


def median(values: Iterable[float]) -> float:
    """Return the middle value, or the mean of the two middle values."""
    ordered = sorted(sample(values))
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2.0


def mode(values: Iterable[float]) -> list[float]:
    """Return all most-frequent values in ascending order.

    A sample in which every value occurs once has no mode and returns ``[]``.
    """
    data = sample(values)
    counts = Counter(data)
    highest = max(counts.values())
    if highest == 1:
        return []
    return sorted(value for value, count in counts.items() if count == highest)


def variance(values: Iterable[float], *, sample_variance: bool = True) -> float:
    """Return sample variance by default, or population variance if requested."""
    data = sample(values)
    denominator = len(data) - 1 if sample_variance else len(data)
    if denominator <= 0:
        raise ValueError("sample variance requires at least two observations")
    center = _mean(data)
    return math.fsum((value - center) ** 2 for value in data) / denominator


def standard_deviation(values: Iterable[float], *, sample_variance: bool = True) -> float:
    """Return the square root of sample (default) or population variance."""
    return math.sqrt(variance(values, sample_variance=sample_variance))
