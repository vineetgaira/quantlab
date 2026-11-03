"""Input validation and numerical helpers for long-only portfolio methods."""

import math
from collections.abc import Iterable, Sequence


def validate_returns(observations: Iterable[Iterable[float]]) -> list[list[float]]:
    try:
        data = [[float(value) for value in row] for row in observations]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("observations must be a finite numeric matrix") from exc
    if len(data) < 2 or not data[0] or any(len(row) != len(data[0]) for row in data):
        raise ValueError("observations must have at least two rows and one asset column")
    if any(not math.isfinite(value) for row in data for value in row):
        raise ValueError("observations must contain finite values")
    return data


def validate_covariance(matrix: Sequence[Sequence[float]]) -> list[list[float]]:
    try:
        cov = [[float(value) for value in row] for row in matrix]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("covariance must be a finite numeric square matrix") from exc
    n = len(cov)
    if n == 0 or any(len(row) != n for row in cov):
        raise ValueError("covariance must be a non-empty square matrix")
    if any(not math.isfinite(value) for row in cov for value in row):
        raise ValueError("covariance must contain finite values")
    scale = max(1.0, max(abs(value) for row in cov for value in row))
    for i in range(n):
        if cov[i][i] < -1e-12 * scale:
            raise ValueError("covariance diagonal entries must be non-negative")
        for j in range(i):
            if abs(cov[i][j] - cov[j][i]) > 1e-10 * scale:
                raise ValueError("covariance matrix must be symmetric")
    return cov


def validate_asset_inputs(
    expected_returns: Sequence[float], covariance: Sequence[Sequence[float]],
) -> tuple[list[float], list[list[float]]]:
    cov = validate_covariance(covariance)
    try:
        returns = [float(value) for value in expected_returns]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("expected_returns must contain finite numbers") from exc
    if len(returns) != len(cov) or not all(math.isfinite(value) for value in returns):
        raise ValueError("expected_returns must match covariance dimensions and be finite")
    return returns, cov


def project_simplex(values: Sequence[float]) -> list[float]:
    """Euclidean projection onto non-negative weights summing to one."""
    ordered = sorted(values, reverse=True)
    cumulative = 0.0
    rho = 0
    for index, value in enumerate(ordered, 1):
        cumulative += value
        if value - (cumulative - 1.0) / index > 0:
            rho = index
    threshold = (sum(ordered[:rho]) - 1.0) / rho
    return [max(value - threshold, 0.0) for value in values]


def project_target(
    point: Sequence[float], returns: Sequence[float], target: float,
    tolerance: float = 1e-11, max_iter: int = 500,
) -> list[float]:
    """Dykstra projection onto the simplex intersected with a return hyperplane."""
    low, high = min(returns), max(returns)
    if target < low - tolerance or target > high + tolerance:
        raise ValueError("target return must lie between the asset expected returns")
    if high - low < tolerance:
        if abs(target - low) > tolerance:
            raise ValueError("target return is infeasible")
        return project_simplex(point)
    x = list(point)
    p = [0.0] * len(x)
    q = [0.0] * len(x)
    # Projection onto {w: sum(w)=1, returns.w=target} by solving its 2x2 system.
    mu = sum(returns) / len(returns)
    centered = [value - mu for value in returns]
    centered_norm_sq = sum(value * value for value in centered)
    for _ in range(max_iter):
        previous = x
        y = project_simplex([x[i] + p[i] for i in range(len(x))])
        p = [x[i] + p[i] - y[i] for i in range(len(x))]
        z_input = [y[i] + q[i] for i in range(len(x))]
        return_residual = target - mu - sum(
            centered[i] * z_input[i] for i in range(len(x))
        )
        z = [
            z_input[i] + return_residual * centered[i] / centered_norm_sq
            for i in range(len(x))
        ]
        q = [z_input[i] - z[i] for i in range(len(x))]
        x = z
        if max(abs(x[i] - previous[i]) for i in range(len(x))) <= tolerance:
            break
    x = project_simplex(x)
    realized = sum(x[i] * returns[i] for i in range(len(x)))
    if abs(realized - target) > 1e-7 * max(1.0, abs(target)):
        raise ValueError("could not project onto feasible target-return set")
    return x


def portfolio_variance(weights: Sequence[float], covariance: Sequence[Sequence[float]]) -> float:
    return sum(weights[i] * covariance[i][j] * weights[j] for i in range(len(weights)) for j in range(len(weights)))


def validate_weights(weights: Sequence[float], size: int) -> list[float]:
    try:
        result = [float(value) for value in weights]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("weights must contain finite numbers") from exc
    if len(result) != size or any(not math.isfinite(value) or value < 0 for value in result):
        raise ValueError("weights must be finite, non-negative, and match asset count")
    if not math.isclose(sum(result), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("weights must sum to 1")
    return result
