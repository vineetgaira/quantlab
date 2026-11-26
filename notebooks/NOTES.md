# QuantLab study notes

The `notebooks/` directory currently has no `.ipynb` files. These notes are a
topic guide to the subjects implemented in the project, based on the module
documentation and source. They are intended as a compact reference alongside
the code, rather than as a claim that notebooks already exist.

## 1. Root finding

Root finding solves `f(x) = 0`.

- **Bisection:** Start with `[a, b]` where a continuous `f` changes sign. Keep
  the half interval that still brackets the root. It is dependable and halves
  the uncertainty each step, but convergence is linear and requires a bracket.
- **False position (regula falsi):** Use the secant through `(a, f(a))` and
  `(b, f(b))` to estimate a root, while retaining a sign-changing bracket. It
  can be faster than bisection, though one endpoint can remain fixed for many
  steps.
- **Newton–Raphson:** Iterate `x[n+1] = x[n] - f(x[n])/f'(x[n])`. It is often
  fast near a simple root but needs a derivative and a suitable starting point;
  a zero or small derivative can cause failure.
- **Secant:** Approximate the derivative with two recent points. It avoids an
  explicit derivative but does not preserve a bracket and can diverge.

Always check convergence criteria and the returned residual. A tolerance on
`|f(x)|` measures function error, not necessarily the distance to a root.

## 2. Numerical integration

Numerical quadrature approximates `integral_a^b f(x) dx` by weighted samples.
With `n` equal subintervals, `h = (b-a)/n`.

- **Composite trapezoidal:** Sum trapezoid areas. For smooth functions, global
  error is typically `O(h^2)`; it works with any positive `n`.
- **Composite Simpson 1/3:** Fit parabolas over pairs of subintervals. Its
  composite form requires even `n` and has typical smooth-function error
  `O(h^4)`.
- **Composite Simpson 3/8:** Fit cubics over groups of three subintervals. It
  requires `n` divisible by three and also typically has `O(h^4)` error.

Both Simpson formulas integrate polynomials through degree three exactly in
exact arithmetic. None of the rules automatically detect discontinuities or
singularities. Reversing integration limits reverses the sign.

## 3. Ordinary differential equations

An initial-value problem has the form `dy/dt = f(t, y)`, with known `y(t0) =
y0`. A step size `h` advances an approximate solution across time.

- **Euler:** `y[n+1] = y[n] + h f(t[n], y[n])`. It uses one slope per step and
  has first-order global accuracy. It is simple, but accuracy and stability
  can require small steps.
- **Classical RK4:** Evaluate slopes at the start, two midpoints, and end of
  each step, then combine them with weights `1, 2, 2, 1` divided by six. It
  generally has fourth-order global accuracy for smooth solutions.

The project shortens the last step to include the requested endpoint. Neither
solver automatically estimates error or adapts its step size; compare results
at successively smaller `h` when assessing numerical accuracy.

## 4. Linear algebra

Many numerical and portfolio problems reduce to solving `A x = b`.

- **Gaussian elimination:** Use row operations to make `A` upper triangular,
  then back-substitute. Partial pivoting swaps rows to reduce instability.
- **LU decomposition:** Factor with pivoting as `P A = L U`. Reuse the factors
  for many right-hand sides by solving two triangular systems.
- **Jacobi iteration:** Compute each new component using only values from the
  previous iterate.
- **Gauss–Seidel iteration:** Reuse newly computed components immediately
  within an iteration, often improving convergence.

Jacobi and Gauss–Seidel stop when the infinity norm of the change between
iterates is small. Convergence is not guaranteed for every matrix; strict
diagonal dominance is a common sufficient condition. Singular systems cannot
be solved uniquely by the direct methods.

## 5. Statistics

- **Mean, median, mode:** Describe center using arithmetic average, middle
  observation, and most frequent value(s). The mean is sensitive to outliers;
  the median is more robust.
- **Variance and standard deviation:** Measure dispersion. Sample variance
  divides squared deviations by `n-1`; population variance divides by `n`.
- **Covariance:** Measures whether paired observations move together, but its
  scale depends on the units. **Pearson correlation** normalizes covariance
  into `[-1, 1]`; it is undefined when either variable is constant.
- **Simple linear regression:** Fit `y = intercept + slope*x` by least squares.
  `R²` summarizes the fraction of observed variation explained in this sample;
  it does not establish causation or guarantee predictive performance.
- **One-sample t-test:** Tests a sample mean against a specified population
  mean. **Welch's two-sample t-test** compares independent means without
  assuming equal variances. Both return a t statistic, degrees of freedom, and
  two-sided p-value.

Statistical conclusions depend on assumptions such as independent observations
and, for these small-sample t procedures, approximate normality. A p-value is
not the probability that the null hypothesis is true.

## 6. Monte Carlo simulation and geometric Brownian motion

Geometric Brownian motion (GBM) models a positive price with drift and random
proportional shocks. For a time increment `dt`, the exact transition used here
is:

`S(t+dt) = S(t) exp((mu - sigma^2/2)dt + sigma sqrt(dt) Z)`,

where `Z` is standard normal, `mu` is annualized drift, and `sigma` is
annualized volatility. Simulating many independent paths approximates a
distribution of outcomes; a seed makes a run reproducible.

Distribution summaries report sample mean, standard deviation, standard error,
and an approximate normal confidence interval for the mean. Simulation is
conditional on model assumptions: more paths reduce Monte Carlo noise but do
not fix a misspecified model. Normal intervals can be poor for small samples or
strongly non-normal outcomes.

## 7. Option pricing

The project prices European calls and puts under no dividends and a
continuously compounded risk-free rate.

- **Black–Scholes:** Uses spot `S`, strike `K`, time `T`, rate `r`, and
  volatility `sigma`; the standard terms are `d1 = [ln(S/K) + (r +
  sigma²/2)T]/(sigma sqrt(T))` and `d2 = d1 - sigma sqrt(T)`. A call price is
  `S N(d1) - K exp(-rT)N(d2)`; a put is `K exp(-rT)N(-d2) - S N(-d1)`.
- **Greeks:** Delta measures price sensitivity to spot; gamma is the change in
  delta; vega measures sensitivity to volatility; theta measures time decay.
  In this project vega is per 1.00 volatility change and theta is annual.
- **CRR binomial tree:** Model up/down moves over discrete steps, price terminal
  payoffs, then discount backward using risk-neutral probabilities. More steps
  generally refine the approximation; incompatible probabilities are invalid.

These are model values, not guaranteed market prices. Their assumptions omit
features such as dividends, early exercise, transaction costs, and changing
volatility. The implementation handles expiry and zero volatility separately.

## 8. Portfolio optimization and analytics

For asset weights `w`, expected returns `mu`, and covariance matrix `Sigma`,
portfolio expected return is `wᵀmu` and variance is `wᵀSigma w`. Volatility is
the square root of variance. The Sharpe ratio is excess return over the
risk-free rate divided by volatility.

The project assumes long-only, fully invested portfolios: weights are
nonnegative and sum to one. It estimates covariance from historical return
rows and uses numerical projected-gradient methods to find a minimum-variance
portfolio, a maximum-Sharpe portfolio, and portfolios along an efficient
frontier. The frontier shows the best modeled return for a range of risk
levels (or equivalently the lowest variance for target returns).

Expected returns and covariance must use the same asset order and time period.
Optimization results are sensitive to estimation error and covariance quality;
historical estimates do not predict future returns. Inspect inputs and
constraints before interpreting a numerical optimum.

## 9. Backtesting

A backtest applies a strategy to historical prices to simulate an equity
curve. The strategy callback sees data only through the current close; its
target exposure earns the next close-to-close return. Exposure `1` means fully
long, `0` flat, and `-1` fully short. The engine charges a transaction cost
based on absolute exposure change and liquidates at the end.

Common performance measures include:

- **CAGR:** Annualized compound growth rate over the test period.
- **Annualized volatility:** Standard deviation of periodic returns scaled by
  the number of periods per year.
- **Sharpe ratio:** Annualized excess return per unit of return volatility.
- **Maximum drawdown:** Largest peak-to-trough percentage loss.
- **Calmar ratio:** CAGR divided by the magnitude of maximum drawdown.

Backtests assume equally spaced observations. Results can be overstated by
look-ahead bias, survivorship bias, data snooping, or unrealistic execution.
The engine does not model slippage, taxes, borrowing costs, margin, or market
impact, so add suitable assumptions before treating results as actionable.

## 10. Financial machine learning

- **Feature engineering:** Lagged returns and rolling sample volatility can
  summarize recent history. A prediction target should be in the future
  relative to its features; transformations must not use future observations.
- **Linear return model:** Fits ordinary least squares with an intercept and
  standardized features using gradient descent. Scaling matters because
  optimization and regularization behavior depend on feature magnitudes.
- **GARCH(1,1)-inspired volatility model:** Updates conditional variance from
  a constant, the previous squared shock, and previous variance. Persistence
  below one is used for a stable long-run variance. Forecasts share the input
  returns' time period and scale.
- **Regime detection:** K-means groups observations by Euclidean distance.
  Scale features comparably first. Cluster numbers are identifiers, not
  automatic labels such as bull or bear.
- **Time-series validation:** Expanding-window splits train on earlier data
  and test on later data. Reported measures include MAE, RMSE, and directional
  accuracy. Fit data-dependent preprocessing within each training fold to
  avoid leakage.

Financial returns are noisy and nonstationary. Validation on chronological
holdouts is essential, and good historical scores do not assure future results.

## 11. Visualization and reporting

The visualization package analyzes a price series, displays prices and
periodic returns, and reports total return, annualized return, volatility, and
maximum drawdown. It can produce an interactive HTML dashboard, a Streamlit
interface, and HTML or one-page PDF reports. CSV input recognizes common price
column names (`price`, `close`, `adj close`, `adj_close`) and optional date or
timestamp labels.

Charts make patterns easier to inspect but do not validate a strategy or
statistical claim. Check date ordering, missing values, units, return
conventions, and annualization frequency before interpreting the visuals.
Interactive browser charts load Plotly.js from a CDN; Streamlit is an optional
dependency.

## Suggested reading order

1. Root finding, integration, differential equations, and linear algebra.
2. Descriptive statistics, association, regression, and hypothesis tests.
3. Simulation and option pricing.
4. Portfolio optimization, backtesting, and financial machine learning.
5. Visualization and reporting.

For implementation details and function signatures, see the guides in
[`../docs/`](../docs/index.md) and the corresponding packages under `../src/`.
