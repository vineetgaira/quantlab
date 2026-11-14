# QuantLab

> A Python toolkit for quantitative research, numerical methods, portfolio analysis, and visualization.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange)]()
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Docs](https://img.shields.io/badge/Docs-Available-brightgreen)](docs/index.md)

---

## Overview

QuantLab is a modular Python project for quantitative research. The repository
currently contains tested implementations for numerical methods, statistics,
simulation, option pricing, portfolio optimization, backtesting, machine
learning utilities, and visualization. A financial data layer and a dedicated
risk analytics package remain on the roadmap.

The project is in active development. See the [documentation index](docs/index.md)
for guides and examples for the implemented modules.

---

## Implemented modules

| Module | Current capabilities |
|---|---|
| `src.roots` | Bisection, Newton–Raphson, secant, and false-position root finding |
| `src.numerical_integration` | Composite trapezoidal, Simpson's 1/3, and Simpson's 3/8 rules |
| `src.differential_equations` | Euler and classical fourth-order Runge–Kutta initial-value solvers |
| `src.linear_algebra` | Gaussian elimination, LU decomposition, Jacobi, and Gauss–Seidel methods |
| `src.statistics` | Descriptive statistics, covariance, correlation, regression, and t-tests |
| `src.simulation` | Geometric Brownian motion paths and distribution summaries |
| `src.option_pricing` | Black–Scholes prices and Greeks, plus CRR binomial pricing |
| `src.portfolio_optimization` | Covariance, mean-variance optimization, efficient frontier, and portfolio metrics |
| `src.backtesting` | Strategy interface, backtest engine, trades, and performance metrics |
| `src.machine_learning` | Return features/models, volatility model, regime detection, and time-series evaluation |
| `src.visualization` | Price analytics, interactive charts, Streamlit dashboard, and HTML/PDF reports |

The Python algorithms use the standard library. The optional dashboard uses
Streamlit, and its interactive browser charts load Plotly.js from a CDN.

---

## Project structure

```text
quantlab/
├── src/
│   ├── roots/                       # Scalar root-finding methods
│   ├── numerical_integration/       # Composite quadrature rules
│   ├── differential_equations/      # Scalar initial-value ODE solvers
│   ├── linear_algebra/              # Direct and iterative solvers
│   ├── statistics/                  # Descriptive and inferential statistics
│   ├── simulation/                  # GBM simulation and distribution analysis
│   ├── option_pricing/              # Black–Scholes and binomial pricing
│   ├── portfolio_optimization/      # Mean-variance tools and analytics
│   ├── backtesting/                 # Strategy backtesting and metrics
│   ├── machine_learning/             # Features, models, regimes, evaluation
│   └── visualization/               # Dashboard, CSV input, HTML/PDF reports
├── tests/                            # Pytest module tests
├── docs/                             # Module guides
├── app.py                            # Small project entry point
├── pyproject.toml                    # Package metadata and pytest configuration
├── requirements.txt                  # Test dependency
├── LICENSE
└── README.md
```

Modules are imported from the `src` namespace, for example `from src.roots
import bisection_method`.

---

## Development roadmap

### Phase 0 — Project foundation

- [x] Repository and project structure
- [x] Python package metadata and test configuration
- [x] Documentation setup
- [ ] Contribution and development standards
- [ ] Linting and pre-commit hooks
- [ ] Continuous integration workflow

### Phase 1 — Numerical methods

- [x] Bisection, Newton–Raphson, secant, and false-position methods
- [x] Trapezoidal rule and Simpson's 1/3 and 3/8 rules
- [x] Euler and fourth-order Runge–Kutta methods
- [x] Gaussian elimination and LU decomposition
- [x] Jacobi and Gauss–Seidel iterative methods

### Phase 2 — Statistics engine

- [x] Mean, median, mode, variance, and standard deviation
- [x] Covariance and correlation
- [x] Simple linear regression
- [x] One-sample and Welch two-sample t-tests

### Phase 3 — Financial data layer

- [ ] Market data loader for CSV and APIs
- [ ] Data cleaning pipeline
- [ ] Arithmetic and log returns
- [ ] Drawdown analysis module

### Phase 4 — Risk analytics

- [ ] Historical and realized volatility
- [ ] Sharpe and Sortino ratios
- [ ] Maximum drawdown module
- [ ] Historical and parametric value at risk

### Phase 5 — Monte Carlo simulation

- [x] Geometric Brownian motion
- [x] Multi-path simulation
- [x] Distribution summaries and confidence intervals

### Phase 6 — Option pricing

- [x] Black–Scholes call and put pricing
- [x] Delta, gamma, vega, and theta
- [x] Cox–Ross–Rubinstein binomial pricing

### Phase 7 — Portfolio optimization

- [x] Asset covariance matrix
- [x] Efficient frontier
- [x] Minimum-variance and maximum-Sharpe portfolios
- [x] Portfolio performance analytics

### Phase 8 — Backtesting engine

- [x] Strategy base interface and backtest engine
- [x] CAGR, Sharpe, Calmar, volatility, and drawdown metrics
- [x] Trade events, trade log, and trade-level analytics

### Phase 9 — Machine learning

- [x] Return feature engineering
- [x] Return prediction model
- [x] GARCH-inspired volatility model
- [x] Market regime detection
- [x] Time-series cross-validation and evaluation

### Phase 10 — Visualization dashboard

- [x] Interactive price and return charts
- [x] Analytics dashboard layout
- [x] Streamlit application with CSV upload
- [x] HTML and PDF report generation

---

## Technology and dependencies

| Technology | Use | Status |
|---|---|---|
| Python 3.11+ | Core language | Required |
| Python standard library | Core algorithms, analytics, and reports | Required |
| Pytest | Test suite | Development requirement (`requirements.txt`) |
| Streamlit | Optional dashboard interface | Install with the `dashboard` extra |
| Plotly.js | Interactive charts in browser | Loaded from CDN by the dashboard |

NumPy, Pandas, Matplotlib, SciPy, SymPy, and Scikit-learn are not current
runtime dependencies.

---

## Getting started

```bash
git clone https://github.com/yourusername/quantlab.git
cd quantlab
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows PowerShell
python -m pip install -e .
python -m pip install -r requirements.txt
```

To install and launch the optional visualization app:

```bash
python -m pip install -e '.[dashboard]'
streamlit run src/visualization/streamlit_app.py
```

The dashboard accepts a CSV containing a `price`, `close`, `adj close`, or
`adj_close` column. A `date`, `timestamp`, or `datetime` column can provide
chart labels.

---

## Running tests

From the repository root:

```bash
python -m pytest
```

---

## Current status

**Implemented:** Phases 1, 2, and 5–10 have source modules, documentation, and
tests. Phase 0 has package metadata and pytest configuration; contribution
standards, linting, and CI remain open. Phases 3 and 4 have not been implemented
as dedicated modules yet.

**Current focus:** Build the financial data layer (Phase 3), then risk analytics
(Phase 4).

---

## Documentation

Start at the [documentation index](docs/index.md) for module guides, API usage,
and examples.

## Contributing

QuantLab is an early-stage research project. Contribution and development
guidelines have not been established yet.

## License

This project is licensed under the [MIT License](LICENSE).
