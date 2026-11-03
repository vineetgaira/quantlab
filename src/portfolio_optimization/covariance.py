"""Covariance matrix estimation from asset return observations."""

import math
from collections.abc import Iterable

from .core import validate_returns


def asset_covariance_matrix(
    observations: Iterable[Iterable[float]], *, sample_covariance: bool = True
) -> list[list[float]]:
    """Estimate a symmetric asset covariance matrix from row-wise observations.

    Rows represent time observations and columns represent assets. The sample
    estimator (denominator ``n - 1``) is used by default; set
    ``sample_covariance=False`` for a population estimator.
    """
    data = validate_returns(observations)
    n_obs, n_assets = len(data), len(data[0])
    denominator = n_obs - 1 if sample_covariance else n_obs
    means = [math.fsum(row[j] for row in data) / n_obs for j in range(n_assets)]
    return [
        [
            math.fsum((row[i] - means[i]) * (row[j] - means[j]) for row in data)
            / denominator
            for j in range(n_assets)
        ]
        for i in range(n_assets)
    ]
