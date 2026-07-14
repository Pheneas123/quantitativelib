import numpy as np
import pandas as pd
import pytest

from quantitativelib.stats import risk_metrics


def test_risk_metrics_uses_the_lower_tail_for_expected_shortfall():
    returns = pd.Series([-0.10, -0.05, -0.02, 0.01, 0.03])

    result = risk_metrics(returns=returns, alpha=0.4)

    assert result["VaR"] == pytest.approx(returns.quantile(0.4))
    assert result["ES"] == pytest.approx(returns[returns <= returns.quantile(0.4)].mean())
    assert result["ES"] <= result["VaR"]


def test_risk_metrics_can_report_positive_loss_magnitudes():
    returns = [-0.10, -0.05, -0.02, 0.01, 0.03]

    signed = risk_metrics(returns=returns, alpha=0.4)
    positive = risk_metrics(returns=returns, alpha=0.4, force_positive=True)

    assert positive["VaR"] == pytest.approx(abs(signed["VaR"]))
    assert positive["ES"] == pytest.approx(abs(signed["ES"]))
    assert positive["VaR_annualised"] == pytest.approx(positive["VaR"] * np.sqrt(252))


@pytest.mark.parametrize("alpha", [0, 1, -0.1, 1.1])
def test_risk_metrics_rejects_invalid_alpha(alpha):
    with pytest.raises(ValueError, match="alpha must be between"):
        risk_metrics(returns=[-0.01, 0.01], alpha=alpha)


def test_risk_metrics_rejects_empty_returns():
    with pytest.raises(ValueError, match="No returns data"):
        risk_metrics(returns=[])
