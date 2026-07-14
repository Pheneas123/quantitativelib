# quantitativelib user guide

This guide covers the main workflows in `quantitativelib`. Rates, dividend yields,
returns, and volatilities are expressed as decimals unless stated otherwise, so
5% is passed as `0.05`.

## Installation

```bash
pip install quantitativelib
```

## Option pricing

Use `black_scholes` to calculate prices and Greeks for one or more contracts.

```python
from quantitativelib import black_scholes

result = black_scholes(
    option_type=["call", "put", "binary_call"],
    S=105,
    K=100,
    T=1.0,
    r=0.03,
    sigma=0.20,
    q=0.01,
)
print(result)
```

Supported contract names are `call`, `put`, `forward`, `binary_call`, and
`binary_put`. The result is a pandas DataFrame whose rows contain price, delta,
gamma, vega, rho, and theta. `forward` reports the present value of a forward
contract with delivery price `K`.

Individual pricing functions are also available for calculations that do not
need a table:

```python
from quantitativelib import bs_call_price, bs_call_delta

price = bs_call_price(105, 100, 1.0, 0.03, 0.20, q=0.01)
delta = bs_call_delta(105, 100, 1.0, 0.03, 0.20, q=0.01)
```

## Stochastic simulations

`simulate_sde` provides a single interface for GBM, CIR, Ornstein–Uhlenbeck,
Heston, and Merton jump-diffusion paths.

```python
from quantitativelib import simulate_sde

t, path = simulate_sde(
    "gbm",
    params={"S0": 100, "mu": 0.05, "sigma": 0.20},
    T=1.0,
    N=252,
    method="milstein",
    seed=42,
    plot=False,
)
```

For CIR and OU, `method` can also be `euler` or `milstein`. Heston returns three
arrays instead of two:

```python
t, price, variance = simulate_sde(
    "heston",
    params={
        "S0": 100,
        "V0": 0.04,
        "mu": 0.05,
        "kappa": 1.5,
        "theta": 0.04,
        "xi": 0.30,
        "rho": -0.7,
    },
    N=252,
    seed=42,
    plot=False,
)
```

Set `return_stats=True` to append summary statistics to the return tuple. For
Heston these include final and path-average price and variance. A seed makes
results repeatable, but the current API sets NumPy's global random seed.

## Historical analysis

`analyse` downloads adjusted prices from Yahoo Finance, calculates daily returns
and summary statistics, and can display price and return plots.

```python
from quantitativelib import analyse

summary = analyse(
    ["AAPL", "MSFT"],
    start_date="2023-01-01",
    end_date="2024-01-01",
    stats=["mean", "std", "sharpe", "cumulative", "drawdown"],
    show_plots=False,
    show_stats=False,
)
```

This workflow requires internet access and depends on Yahoo Finance data and
symbol conventions.

## Historical VaR and expected shortfall

Pass a return series when data is already available:

```python
import pandas as pd
from quantitativelib import risk_metrics

returns = pd.Series([-0.012, 0.004, -0.021, 0.008, -0.006])
risk = risk_metrics(returns=returns, alpha=0.05)
```

`VaR` is the empirical lower-tail quantile and `ES` is the mean of observations
at or below that quantile. They are negative return thresholds by default. Set
`force_positive=True` to report loss magnitudes instead. The annualised fields
use square-root-of-time scaling.

Alternatively, provide `ticker`, `start_date`, and `end_date` to download prices.

## GARCH volatility

The high-level workflow fits a zero-mean GARCH(1,1), forecasts variance, and runs
a rolling backtest:

```python
from quantitativelib import analyse_volatility

result = analyse_volatility(
    returns=returns,
    horizon=5,
    window=250,
    refit=20,
    dist="t",
    plot=False,
)

fit = result["fit"]
forecast = result["forecast"]
backtest = result["backtest"]
```

The rolling backtest refits parameters every `refit` observations and updates the
conditional variance at every forecast origin. Forecast horizon `h` is evaluated
against the return `h` observations after that origin.

Lower-level functions `fit_garch`, `forecast_garch`, and `backtest_garch` are
available when the three stages need to be controlled separately.

## Plot configuration

Plotting functions call `matplotlib.pyplot.show()`. For batch jobs and automated
tests, pass `plot=False` or `show_plots=False`. `simulate_sde` accepts line styles
through `plot_config`; `analyse` accepts pandas plotting options through
`plot_kwargs`; and `analyse_volatility` documents supported modes in its
docstring.

## Limitations

- Pricing functions use the Black–Scholes assumptions and continuous rates.
- Historical risk estimates depend heavily on sample size and are not forecasts.
- Euler-style CIR and Heston discretisations can produce negative simulated
  states; coefficients use truncation where required by square roots.
- GARCH functions assume zero-mean returns and a GARCH(1,1) specification.
- Market-data helpers rely on the external `yfinance` service.

See [API reference](api-reference.md) for signatures and [model notes](model-notes.md)
for formulas and numerical conventions.
