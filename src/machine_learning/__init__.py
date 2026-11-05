"""Feature engineering, prediction, volatility, regimes, and evaluation."""

from .evaluation import (
    CrossValidationResult,
    FoldMetrics,
    cross_validate_regressor,
    time_series_splits,
)
from .features import FeatureSet, build_return_features
from .models import GarchVolatilityModel, LinearReturnModel
from .regimes import RegimeResult, detect_regimes

__all__ = [
    "CrossValidationResult",
    "FeatureSet",
    "FoldMetrics",
    "GarchVolatilityModel",
    "LinearReturnModel",
    "RegimeResult",
    "build_return_features",
    "cross_validate_regressor",
    "detect_regimes",
    "time_series_splits",
]
