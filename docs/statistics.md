# Statistics

The `src.statistics` package contains descriptive statistics, paired association
measures, simple linear regression, and two-sided t tests. Functions accept
iterables of finite numeric values and return Python floats or small immutable
result objects. Empty samples, incompatible lengths, and undefined operations
raise `ValueError`.

```python
from src.statistics import (
    correlation, mean, one_sample_t_test, simple_linear_regression,
)

print(mean([1, 2, 3]))
fit = simple_linear_regression([1, 2, 3], [2, 4, 5])
print(fit.slope, fit.intercept, fit.predict(4))
print(correlation([1, 2, 3], [2, 4, 6]))
print(one_sample_t_test([2.1, 2.4, 1.9, 2.3], population_mean=2.0))
```

## Descriptive statistics

`mean`, `median`, and `mode` compute the arithmetic mean, middle value, and all
most frequent values. `mode` returns an empty list when every observation is
unique. `variance(values, sample_variance=True)` and
`standard_deviation(values, sample_variance=True)` use the sample convention
(denominator `n - 1`) by default; pass `False` for population statistics.
Sample variance requires at least two observations.

## Covariance and correlation

`covariance(x, y, sample_covariance=True)` returns sample covariance by default;
set the flag to `False` for population covariance. `correlation(x, y)` returns
Pearson's correlation coefficient. Paired inputs must have equal length and at
least two observations. Correlation is undefined for constant data and raises
`ValueError` in that case.

## Simple linear regression

`simple_linear_regression(x, y)` fits `y = intercept + slope*x` by ordinary
least squares and returns a `LinearRegressionResult` with `slope`, `intercept`,
`r_squared`, and `predict(x)`. At least two paired observations and two distinct
x values are required.

## Hypothesis tests

`one_sample_t_test(values, population_mean)` tests equality of a sample's
population mean to the supplied value. `welch_t_test(first, second)` compares
two independent means without assuming equal population variances. Both return
a `TestResult` with the t `statistic`, two-sided `p_value`, and
`degrees_of_freedom`. Each sample needs at least two observations and nonzero
variation. The tests assume independent, approximately normally distributed
observations; they do not adjust for multiple comparisons.
