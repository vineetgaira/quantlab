# Machine learning

The `src.machine_learning` package provides dependency-free tools for financial
time-series features, return prediction, volatility forecasting, regime
clustering, and chronological model evaluation.

```python
from src.machine_learning import (
    GarchVolatilityModel, LinearReturnModel, build_return_features,
    cross_validate_regressor, detect_regimes,
)

data = build_return_features(prices, lags=(1, 2, 5), volatility_windows=(5, 20))
scores = cross_validate_regressor(LinearReturnModel, data.features, data.targets)
garch = GarchVolatilityModel.fit(daily_returns)
future_volatility = garch.forecast(10)
regimes = detect_regimes(feature_vectors, n_regimes=3)
```

## Feature engineering and return prediction

`build_return_features(prices, lags=(1, 2, 3), volatility_windows=(5, 20))`
returns a `FeatureSet` containing rows, next-period return targets, and feature
names. Lagged returns and rolling sample volatility use only information
available through each feature timestamp. The next return is the target, which
helps prevent look-ahead leakage.

`LinearReturnModel` fits ordinary least squares with an intercept and
standardized features using gradient descent. Call `fit(features, targets)` and
then `predict(features)`. Inputs are numeric rectangular matrices.

## Volatility forecasting

`GarchVolatilityModel.fit(returns)` estimates a GARCH(1,1) model by a
deterministic conditional-likelihood grid search over `omega`, `alpha`, and
`beta`, with persistence constrained below one. It demeans observations and
models the residuals. `forecast(horizon=1)` returns conditional standard
deviations for future periods. Returns and forecasts must use the same period
and scale.

## Regime detection

`detect_regimes(observations, n_regimes=2, max_iter=100)` clusters rows with
deterministic k-means and returns labels, centroids, and iteration count. Scale
features comparably before clustering because Euclidean distance is sensitive
to units. Labels are ordered by centroid values for repeatability; they are
cluster identifiers, not semantic labels such as “bull” or “bear”.

## Evaluation and cross-validation

`time_series_splits(n_samples, n_splits=5)` produces expanding training
windows and later, non-overlapping test windows. `cross_validate_regressor`
fits a fresh model per fold and reports mean absolute error, root mean squared
error, and directional accuracy. The supplied model factory must return an
object with `fit(features, targets)` and `predict(features)` methods. The split
order preserves time and avoids training on future observations; preprocessing
that learns parameters should likewise be fitted inside each training fold.

All package code uses the Python standard library. Install the project test
dependency with `python -m pip install -r requirements.txt`, then run
`python -m pytest` from the repository root.
