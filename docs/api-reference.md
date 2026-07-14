# API reference

The names below form the intended public surface and can be imported directly
from `quantitativelib`.

## Options

### `black_scholes(option_type, K, S, r, T, sigma, q=0.0, precision=4, show_table=False)`

Returns a DataFrame of prices and Greeks. `option_type` is a string or list
containing `call`, `put`, `forward`, `binary_call`, or `binary_put`.

Low-level functions follow the argument order `(S, K, T, r, sigma, q=0.0)`:

- `bs_call_price`, `bs_call_delta`, `bs_call_gamma`, `bs_call_vega`,
  `bs_call_rho`, `bs_call_theta`
- `bs_put_price`, `bs_put_delta`, `bs_put_gamma`, `bs_put_vega`, `bs_put_rho`,
  `bs_put_theta`
- `bs_binary_call_price`, `bs_binary_call_delta`, `bs_binary_call_gamma`,
  `bs_binary_call_vega`, `bs_binary_call_rho`, `bs_binary_call_theta`
- `bs_binary_put_price`, `bs_binary_put_delta`, `bs_binary_put_gamma`,
  `bs_binary_put_vega`, `bs_binary_put_rho`, `bs_binary_put_theta`

Forward functions omit volatility and follow `(S, K, T, r, q=0.0)`:
`bs_forward_price`, `bs_forward_delta`, `bs_forward_gamma`, `bs_forward_vega`,
`bs_forward_rho`, and `bs_forward_theta`.

## Simulation

### `simulate_sde(model, params, T=1.0, N=1000, method="euler", plot=True, return_stats=False, plot_config=None, seed=None)`

Dispatches to a model simulator. GBM, CIR, OU, and Merton return `(t, X)`.
Heston returns `(t, S, V)`. Enabling statistics appends a dictionary.

Low-level numerical and model functions:

- `euler_maruyama(mu, sigma, X0, T, N, dW=None)`
- `milstein(mu, sigma, sigma_dx, X0, T, N, dW=None)`
- `simulate_gbm(S0, mu, sigma, T, N, method="euler")`
- `simulate_cir(X0, kappa, theta, sigma, T, N, method="euler")`
- `simulate_ou(X0, mu, theta, sigma, T, N, method="euler")`
- `simulate_heston(S0, V0, mu, kappa, theta, xi, rho, T, N)`
- `simulate_merton_jump(S0, mu, sigma, lambd, m, v, T, N)`

## Statistics

### `analyse(ticker, start_date, end_date, ...)`

Downloads adjusted prices and returns a DataFrame of requested summary
statistics. Consult the function docstring for plotting and statistic selectors.

### `risk_metrics(returns=None, ticker=None, start_date=None, end_date=None, risk_free_rate=0.01, alpha=0.05, force_positive=False)`

Calculates empirical historical VaR and expected shortfall. Supply either
`returns` or all three market-data arguments. `risk_free_rate` is retained for
API compatibility and is not currently used in these historical tail estimates.

## Volatility

### `fit_garch(returns, dist="t", options=None)`

Fits a zero-mean GARCH(1,1). Returns parameters, conditional variance,
standardised residuals, convergence information, and the underlying `arch`
result.

### `forecast_garch(fit_result, horizon=1)`

Returns a DataFrame containing variance and volatility forecasts indexed from
horizon 1.

### `backtest_garch(returns, window=1000, horizon=1, refit=20, dist="t", alphas=(0.01, 0.05))`

Runs expanding forecast origins with rolling estimation windows. Returns fitted
parameter snapshots, forecasts, VaR hit indicators, and QLIKE where available.

### `analyse_volatility(...)`

Combines fitting, forecasting, backtesting, optional Yahoo Finance download, and
diagnostic plots. Returns a dictionary with `fit`, `forecast`, and `backtest`.
