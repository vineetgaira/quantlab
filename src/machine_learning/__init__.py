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
    "FeatureSet", "build_return_features", "LinearReturnModel",
    "GarchVolatilityModel", "RegimeResult", "detect_regimes", "FoldMetrics",
    "CrossValidationResult", "time_series_splits", "cross_validate_regressor",
]
