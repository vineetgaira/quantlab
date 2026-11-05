"""Expanding-window cross-validation for numeric regression models."""

import math
from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class FoldMetrics:
    """Regression scores and index ranges for one chronological fold."""

    train_indices: tuple[int, ...]
    test_indices: tuple[int, ...]
    mae: float
    rmse: float
    directional_accuracy: float


@dataclass(frozen=True)
class CrossValidationResult:
    """Per-fold scores and their arithmetic mean."""

    folds: tuple[FoldMetrics, ...]
    mean_mae: float
    mean_rmse: float
    mean_directional_accuracy: float


def time_series_splits(n_samples: int, n_splits: int = 5) -> Iterator[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Yield expanding training windows followed by non-overlapping test windows."""
    if isinstance(n_samples, bool) or not isinstance(n_samples, int) or n_samples < 2:
        raise ValueError("n_samples must be an integer of at least 2")
    if isinstance(n_splits, bool) or not isinstance(n_splits, int) or n_splits < 1:
        raise ValueError("n_splits must be a positive integer")
    test_size = n_samples // (n_splits + 1)
    if test_size < 1:
        raise ValueError("n_samples must be at least n_splits + 1")
    first_test = n_samples - test_size * n_splits
    for fold in range(n_splits):
        test_start = first_test + fold * test_size
        yield tuple(range(test_start)), tuple(range(test_start, test_start + test_size))


def cross_validate_regressor(
    model_factory: Callable[[], object],
    features: Iterable[Iterable[float]],
    targets: Sequence[float],
    n_splits: int = 5,
) -> CrossValidationResult:
    """Evaluate a fresh ``fit``/``predict`` model with expanding time splits."""
    try:
        x = [[float(value) for value in row] for row in features]
        y = [float(value) for value in targets]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("features and targets must be finite numeric values") from exc
    if not x or len(x) != len(y) or any(len(row) != len(x[0]) for row in x):
        raise ValueError("features must be a non-empty rectangular matrix matching targets")
    if any(not math.isfinite(value) for row in x for value in row) or any(
        not math.isfinite(value) for value in y
    ):
        raise ValueError("features and targets must be finite")
    if not callable(model_factory):
        raise ValueError("model_factory must be callable")
    fold_results = []
    for train, test in time_series_splits(len(y), n_splits):
        model = model_factory()
        if not callable(getattr(model, "fit", None)) or not callable(getattr(model, "predict", None)):
            raise ValueError("model_factory must create an object with fit and predict methods")
        model.fit([x[i] for i in train], [y[i] for i in train])
        predicted = [float(value) for value in model.predict([x[i] for i in test])]
        if len(predicted) != len(test) or any(not math.isfinite(value) for value in predicted):
            raise ValueError("model predictions must be finite and match test size")
        errors = [predicted[j] - y[index] for j, index in enumerate(test)]
        mae = math.fsum(abs(value) for value in errors) / len(errors)
        rmse = math.sqrt(math.fsum(value * value for value in errors) / len(errors))
        directional = sum(
            (predicted[j] >= 0) == (y[index] >= 0) for j, index in enumerate(test)
        ) / len(test)
        fold_results.append(FoldMetrics(train, test, mae, rmse, directional))
    return CrossValidationResult(
        tuple(fold_results),
        math.fsum(fold.mae for fold in fold_results) / len(fold_results),
        math.fsum(fold.rmse for fold in fold_results) / len(fold_results),
        math.fsum(fold.directional_accuracy for fold in fold_results) / len(fold_results),
    )
