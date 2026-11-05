"""Market regime clustering with deterministic k-means."""

import math
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class RegimeResult:
    """Cluster label for each observation and cluster center vectors."""

    labels: tuple[int, ...]
    centroids: tuple[tuple[float, ...], ...]
    iterations: int


def detect_regimes(
    observations: Iterable[Iterable[float]], n_regimes: int = 2, max_iter: int = 100
) -> RegimeResult:
    """Cluster feature observations into regimes using deterministic k-means.

    Features should be scaled comparably before clustering. Centers are
    initialized with a deterministic farthest-point strategy and ordered by
    their first coordinate for stable label interpretation.
    """
    try:
        data = [[float(value) for value in row] for row in observations]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("observations must contain finite numeric rows") from exc
    if not data or not data[0] or any(len(row) != len(data[0]) for row in data):
        raise ValueError("observations must be a non-empty rectangular matrix")
    if any(not math.isfinite(value) for row in data for value in row):
        raise ValueError("observations must contain finite values")
    if isinstance(n_regimes, bool) or not isinstance(n_regimes, int) or not 1 <= n_regimes <= len(data):
        raise ValueError("n_regimes must be between 1 and the observation count")
    if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")

    def distance_sq(left, right):
        return sum((a - b) ** 2 for a, b in zip(left, right))

    centers = [data[0][:]]
    while len(centers) < n_regimes:
        candidate = max(data, key=lambda row: min(distance_sq(row, center) for center in centers))
        if min(distance_sq(candidate, center) for center in centers) == 0:
            raise ValueError("observations must contain at least n_regimes distinct points")
        centers.append(candidate[:])
    labels = [0] * len(data)
    for iteration in range(1, max_iter + 1):
        updated_labels = [
            min(range(n_regimes), key=lambda cluster: distance_sq(row, centers[cluster]))
            for row in data
        ]
        updated_centers = []
        for cluster in range(n_regimes):
            members = [row for row, label in zip(data, updated_labels) if label == cluster]
            if not members:
                updated_centers.append(centers[cluster])
            else:
                updated_centers.append(
                    [math.fsum(row[j] for row in members) / len(members) for j in range(len(data[0]))]
                )
        unchanged = updated_labels == labels and all(
            distance_sq(updated_centers[i], centers[i]) <= 1e-24 for i in range(n_regimes)
        )
        labels, centers = updated_labels, updated_centers
        if unchanged:
            break
    order = sorted(range(n_regimes), key=lambda cluster: tuple(centers[cluster]))
    remap = {old: new for new, old in enumerate(order)}
    return RegimeResult(
        tuple(remap[label] for label in labels),
        tuple(tuple(centers[cluster]) for cluster in order),
        iteration,
    )
