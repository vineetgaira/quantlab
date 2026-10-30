"""Simple ordinary least-squares linear regression."""

import math
from collections.abc import Iterable
from dataclasses import dataclass

from ._common import mean, paired_samples


@dataclass(frozen=True)
class LinearRegressionResult:
    """Fitted line parameters and coefficient of determination."""

    slope: float
    intercept: float
    r_squared: float

    def predict(self, x: float) -> float:
        """Predict a response for a finite scalar input."""
        try:
            value = float(x)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("x must be a finite number") from exc
        if not math.isfinite(value):
            raise ValueError("x must be a finite number")
        return self.intercept + self.slope * value


def simple_linear_regression(
    x: Iterable[float], y: Iterable[float]
) -> LinearRegressionResult:
    """Fit ``y = intercept + slope*x`` by minimizing squared residuals."""
    x_values, y_values = paired_samples(x, y)
    x_mean, y_mean = mean(x_values), mean(y_values)
    x_ss = math.fsum((value - x_mean) ** 2 for value in x_values)
    if x_ss == 0:
        raise ValueError("regression requires at least two distinct x values")
    slope = math.fsum(
        (a - x_mean) * (b - y_mean) for a, b in zip(x_values, y_values)
    ) / x_ss
    intercept = y_mean - slope * x_mean
    y_ss = math.fsum((value - y_mean) ** 2 for value in y_values)
    residual_ss = math.fsum(
        (b - (intercept + slope * a)) ** 2 for a, b in zip(x_values, y_values)
    )
    r_squared = 1.0 if y_ss == 0 else 1.0 - residual_ss / y_ss
    return LinearRegressionResult(slope, intercept, r_squared)
