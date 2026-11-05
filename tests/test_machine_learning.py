import math

import pytest

from src.machine_learning import (
    GarchVolatilityModel,
    LinearReturnModel,
    build_return_features,
    cross_validate_regressor,
    detect_regimes,
    time_series_splits,
)


def test_feature_builder_uses_only_trailing_data_and_next_return_target():
    result = build_return_features([100, 101, 99, 100, 102, 101, 103, 104], lags=(1, 2), volatility_windows=(3,))
    assert result.feature_names == ("return_lag_1", "return_lag_2", "volatility_3")
    assert len(result.features) == len(result.targets) == 4
    assert result.features[0][0] == pytest.approx(100 / 99 - 1)
    assert result.features[0][1] == pytest.approx(99 / 101 - 1)
    assert result.targets[0] == pytest.approx(102 / 100 - 1)


def test_feature_builder_rejects_insufficient_or_invalid_history():
    with pytest.raises(ValueError, match="not enough"):
        build_return_features([100, 101, 102], volatility_windows=(5,))
    with pytest.raises(ValueError, match="positive finite"):
        build_return_features([100, 0, 102])


def test_linear_return_model_fits_and_predicts_linear_relation():
    x = [[float(i), float(i % 3)] for i in range(20)]
    y = [2 * row[0] - 3 * row[1] + 4 for row in x]
    model = LinearReturnModel().fit(x, y)
    assert model.predict([[4, 1], [10, 2]]) == pytest.approx([9, 18], abs=1e-6)


def test_garch_fit_forecasts_positive_volatility():
    returns = [0.01 * math.sin(i * 1.7) + (0.03 if i % 11 == 0 else 0) for i in range(120)]
    model = GarchVolatilityModel.fit(returns)
    forecast = model.forecast(5)
    assert model.omega > 0
    assert 0 <= model.alpha + model.beta < 1
    assert len(forecast) == 5
    assert all(value > 0 and math.isfinite(value) for value in forecast)


def test_regime_clustering_separates_low_and_high_return_groups():
    observations = [[-3.1, 1.0], [-2.9, 1.2], [-3.0, 0.9], [2.9, 1.1], [3.2, 0.8], [3.0, 1.0]]
    result = detect_regimes(observations, n_regimes=2)
    assert len(result.centroids) == 2
    assert result.labels[:3] == (result.labels[0],) * 3
    assert result.labels[3:] == (result.labels[3],) * 3
    assert result.labels[0] != result.labels[3]


def test_time_series_cross_validation_has_expanding_train_windows():
    splits = list(time_series_splits(12, n_splits=3))
    assert splits == [
        (tuple(range(3)), (3, 4, 5)),
        (tuple(range(6)), (6, 7, 8)),
        (tuple(range(9)), (9, 10, 11)),
    ]
    x = [[float(i)] for i in range(12)]
    y = [2 * i + 1 for i in range(12)]
    result = cross_validate_regressor(LinearReturnModel, x, y, n_splits=3)
    assert len(result.folds) == 3
    assert result.mean_mae < 1e-5
    assert result.mean_rmse < 1e-5


def test_ml_components_reject_invalid_inputs():
    with pytest.raises(RuntimeError, match="fitted"):
        LinearReturnModel().predict([[1]])
    with pytest.raises(ValueError, match="non-zero variance"):
        GarchVolatilityModel.fit([0, 0, 0])
    with pytest.raises(ValueError, match="distinct"):
        detect_regimes([[1], [1]], n_regimes=2)
    with pytest.raises(ValueError, match="n_samples"):
        list(time_series_splits(4, n_splits=5))
