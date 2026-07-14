import numpy as np
import pytest

from quantitativelib import base
from quantitativelib.options import black_scholes


def test_call_put_parity_with_dividends():
    S, K, T, r, sigma, q = 105.0, 100.0, 1.25, 0.03, 0.22, 0.01

    call = base.bs_call_price(S, K, T, r, sigma, q)
    put = base.bs_put_price(S, K, T, r, sigma, q)

    expected = S * np.exp(-q * T) - K * np.exp(-r * T)
    assert call - put == pytest.approx(expected)


@pytest.mark.parametrize(
    ("price", "gamma"),
    [
        (base.bs_binary_call_price, base.bs_binary_call_gamma),
        (base.bs_binary_put_price, base.bs_binary_put_gamma),
    ],
)
def test_binary_gamma_matches_price_finite_difference(price, gamma):
    S, K, T, r, sigma, q = 105.0, 100.0, 0.8, 0.025, 0.3, 0.01
    step = 1e-2
    numerical = (
        price(S + step, K, T, r, sigma, q)
        - 2 * price(S, K, T, r, sigma, q)
        + price(S - step, K, T, r, sigma, q)
    ) / step**2

    assert gamma(S, K, T, r, sigma, q) == pytest.approx(numerical, rel=1e-5)


def test_black_scholes_returns_requested_contracts():
    result = black_scholes(
        ["call", "put", "forward"],
        K=100,
        S=105,
        r=0.03,
        T=1,
        sigma=0.2,
        q=0.01,
    )

    assert list(result.columns) == ["Call", "Put", "Forward"]
    assert list(result.index) == ["Price", "Delta", "Gamma", "Vega", "Rho", "Theta"]


def test_black_scholes_rejects_unknown_contract():
    with pytest.raises(ValueError, match="Unknown option type"):
        black_scholes("straddle", K=100, S=100, r=0.03, T=1, sigma=0.2)
