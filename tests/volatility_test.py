import numpy as np
import pandas as pd
import pytest

import quantitativelib.base as base


class FakeResult:
    def __init__(self, sample):
        self.params = pd.Series({"omega": 0.1, "alpha[1]": 0.2, "beta[1]": 0.3})
        self.conditional_volatility = pd.Series(
            np.full(len(sample), np.sqrt(0.4)), index=sample.index
        )


class FakeModel:
    def __init__(self, sample):
        self.sample = sample

    def fit(self, **kwargs):
        return FakeResult(self.sample)


def test_backtest_updates_variance_between_parameter_refits(monkeypatch):
    monkeypatch.setattr(base, "arch_model", lambda sample, **kwargs: FakeModel(sample))
    returns = pd.Series([0.1, -0.2, 0.3, -0.4, 0.5, -0.6], index=pd.date_range("2024-01-01", periods=6))

    result = base.backtest_garch(
        returns, window=3, horizon=1, refit=10, dist="normal", alphas=(0.05,)
    )
    forecasts = result["forecasts"]["variance"].to_numpy()

    first = 0.1 + 0.2 * returns.iloc[2] ** 2 + 0.3 * 0.4
    second = 0.1 + 0.2 * returns.iloc[3] ** 2 + 0.3 * first
    assert forecasts[0] == pytest.approx(first)
    assert forecasts[1] == pytest.approx(second)
    assert forecasts[0] != forecasts[1]


def test_backtest_forecast_dates_are_origins_for_future_returns(monkeypatch):
    monkeypatch.setattr(base, "arch_model", lambda sample, **kwargs: FakeModel(sample))
    index = pd.date_range("2024-01-01", periods=7)
    returns = pd.Series(np.linspace(-0.03, 0.03, 7), index=index)

    result = base.backtest_garch(
        returns, window=3, horizon=2, refit=10, dist="normal", alphas=(0.05,)
    )

    origins = result["forecasts"].index.get_level_values("date").unique()
    assert origins[0] == index[2]
    assert origins[-1] == index[-3]
    assert result["var_hits"].index.get_level_values("horizon").max() == 2


def test_backtest_rejects_invalid_refit(monkeypatch):
    with pytest.raises(ValueError, match="refit must be"):
        base.backtest_garch(pd.Series(np.arange(8.0)), window=3, refit=0)
