"""Small dependency-free prediction and volatility models."""

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass


def _matrix_and_target(
    features: Iterable[Iterable[float]], targets: Iterable[float]
) -> tuple[list[list[float]], list[float]]:
    try:
        x = [[float(value) for value in row] for row in features]
        y = [float(value) for value in targets]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("features and targets must contain finite numbers") from exc
    if not x or not x[0] or len(x) != len(y) or any(len(row) != len(x[0]) for row in x):
        raise ValueError("features must be a non-empty rectangular matrix matching targets")
    if any(not math.isfinite(value) for row in x for value in row) or any(
        not math.isfinite(value) for value in y
    ):
        raise ValueError("features and targets must contain finite numbers")
    return x, y


class LinearReturnModel:
    """Ordinary least squares regression fitted by gradient descent.

    Features are standardized internally for stable optimization. The model
    supports one or more numeric features and includes an intercept.
    """

    def __init__(self, max_iter: int = 20_000, tolerance: float = 1e-10):
        if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter < 1:
            raise ValueError("max_iter must be a positive integer")
        try:
            tolerance = float(tolerance)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("tolerance must be a finite positive number") from exc
        if not math.isfinite(tolerance) or tolerance <= 0:
            raise ValueError("tolerance must be a finite positive number")
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.coefficients: tuple[float, ...] | None = None
        self.intercept: float | None = None
        self._means: tuple[float, ...] | None = None
        self._scales: tuple[float, ...] | None = None

    def fit(self, features: Iterable[Iterable[float]], targets: Iterable[float]) -> "LinearReturnModel":
        x, y = _matrix_and_target(features, targets)
        n, dimensions = len(x), len(x[0])
        means = [math.fsum(row[j] for row in x) / n for j in range(dimensions)]
        scales = [
            math.sqrt(math.fsum((row[j] - means[j]) ** 2 for row in x) / n) or 1.0
            for j in range(dimensions)
        ]
        standardized = [[(row[j] - means[j]) / scales[j] for j in range(dimensions)] for row in x]
        y_mean = math.fsum(y) / n
        centered_y = [value - y_mean for value in y]
        # The standardized columns have mean zero and population variance one.
        weights = [0.0] * dimensions
        step = 0.45 / max(dimensions, 1)
        for _ in range(self.max_iter):
            gradient = [
                2.0 * math.fsum(
                    standardized[i][j]
                    * (sum(weights[k] * standardized[i][k] for k in range(dimensions)) - centered_y[i])
                    for i in range(n)
                ) / n
                for j in range(dimensions)
            ]
            updated = [weights[j] - step * gradient[j] for j in range(dimensions)]
            if max(abs(updated[j] - weights[j]) for j in range(dimensions)) <= self.tolerance:
                weights = updated
                break
            weights = updated
        self._means = tuple(means)
        self._scales = tuple(scales)
        self.coefficients = tuple(weights[j] / scales[j] for j in range(dimensions))
        self.intercept = y_mean - sum(self.coefficients[j] * means[j] for j in range(dimensions))
        return self

    def predict(self, features: Iterable[Iterable[float]]) -> list[float]:
        if self.coefficients is None or self.intercept is None:
            raise RuntimeError("model must be fitted before prediction")
        try:
            rows = [list(row) for row in features]
        except TypeError as exc:
            raise ValueError("features must be a rectangular matrix") from exc
        x, _ = _matrix_and_target(rows, [0.0] * len(rows))
        if len(x[0]) != len(self.coefficients):
            raise ValueError("feature column count does not match fitted model")
        return [self.intercept + sum(a * b for a, b in zip(self.coefficients, row)) for row in x]


@dataclass(frozen=True)
class GarchVolatilityModel:
    """Fitted GARCH(1,1) volatility model parameters and terminal state."""

    omega: float
    alpha: float
    beta: float
    last_variance: float
    last_squared_return: float

    @classmethod
    def fit(cls, returns: Iterable[float]) -> "GarchVolatilityModel":
        """Estimate GARCH(1,1) parameters by a deterministic likelihood grid search."""
        try:
            values = [float(value) for value in returns]
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("returns must contain finite numeric values") from exc
        if len(values) < 3 or any(not math.isfinite(value) for value in values):
            raise ValueError("at least three finite returns are required")
        center = math.fsum(values) / len(values)
        residuals = [value - center for value in values]
        unconditional = math.fsum(value * value for value in residuals) / len(residuals)
        if unconditional <= 0:
            raise ValueError("returns must have non-zero variance")
        best = (math.inf, 0.05, 0.90)
        for alpha_i in range(1, 21):
            alpha = alpha_i * 0.015
            for beta_i in range(10, 66):
                beta = beta_i * 0.015
                if alpha + beta >= 0.995:
                    continue
                omega = unconditional * (1.0 - alpha - beta)
                variance = unconditional
                likelihood = 0.0
                for value in residuals:
                    variance = max(omega + alpha * value * value + beta * variance, 1e-18)
                    likelihood += math.log(variance) + value * value / variance
                if likelihood < best[0]:
                    best = (likelihood, alpha, beta)
        _, alpha, beta = best
        omega = unconditional * (1.0 - alpha - beta)
        variance = unconditional
        for value in residuals:
            variance = max(omega + alpha * value * value + beta * variance, 1e-18)
        return cls(omega, alpha, beta, variance, residuals[-1] ** 2)

    def forecast(self, horizon: int = 1) -> list[float]:
        """Forecast conditional volatility for each future step."""
        if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 1:
            raise ValueError("horizon must be a positive integer")
        variances = []
        variance = self.omega + self.alpha * self.last_squared_return + self.beta * self.last_variance
        for _ in range(horizon):
            variance = max(variance, 0.0)
            variances.append(math.sqrt(variance))
            variance = self.omega + (self.alpha + self.beta) * variance
        return variances
