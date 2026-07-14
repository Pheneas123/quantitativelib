# Model and numerical notes

## Black–Scholes conventions

The option functions use spot `S`, strike `K`, time in years `T`, continuously
compounded risk-free rate `r`, volatility `sigma`, and continuous dividend yield
`q`. Cash-or-nothing binary options pay one unit at maturity.

Greeks are raw derivatives with respect to their inputs. Vega and rho are per
unit change, not per percentage point. Theta is the calendar-time decay
convention implemented by the formulas.

## Stochastic processes

GBM, CIR, and OU can use Euler–Maruyama or Milstein discretisation. Heston uses a
correlated Euler step for price and variance. Merton jump diffusion samples a
Poisson jump count per step and normally distributed aggregate log jumps.

These functions return a single simulated path. They do not currently provide a
vectorised Monte Carlo path dimension, confidence intervals, or variance
reduction.

## Historical risk

For significance level `alpha`, historical VaR is the empirical `alpha`
quantile. Expected shortfall is the arithmetic mean of sample returns less than
or equal to that quantile. Negative values represent losses; positive reporting
uses absolute magnitudes.

Square-root-of-252 annualisation is provided for convenience. This scaling is a
model assumption and can be inappropriate for autocorrelated or heavy-tailed
returns.

## GARCH backtesting

The implemented model is

```text
h[t+1] = omega + alpha * r[t]^2 + beta * h[t]
```

Parameters are refitted using the most recent `window` returns every `refit`
forecast origins. Between refits, each newly observed return updates conditional
variance using the equation above. Multi-step forecasts replace unknown future
squared returns with their conditional expectation, producing
`omega + (alpha + beta) * h` after horizon 1.

VaR hit indicators compare each horizon forecast with its corresponding future
return. Student-t forecasts use the fitted degrees of freedom and a variance
standardisation factor.
