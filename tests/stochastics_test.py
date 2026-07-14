import numpy as np

from quantitativelib.stochastics import simulate_sde


def test_heston_runs_without_plotting():
    result = simulate_sde(
        "heston",
        params={
            "S0": 100,
            "V0": 0.04,
            "mu": 0.05,
            "kappa": 1.5,
            "theta": 0.04,
            "xi": 0.3,
            "rho": -0.7,
        },
        T=1,
        N=20,
        seed=3,
        plot=False,
    )

    t, price, variance = result
    assert len(t) == len(price) == len(variance) == 21
    assert np.all(np.isfinite(price))
    assert np.all(np.isfinite(variance))


def test_heston_returns_meaningful_path_statistics():
    t, price, variance, stats = simulate_sde(
        "heston",
        params={
            "S0": 100,
            "V0": 0.04,
            "mu": 0.05,
            "kappa": 1.5,
            "theta": 0.04,
            "xi": 0.3,
            "rho": -0.7,
        },
        N=10,
        seed=4,
        plot=False,
        return_stats=True,
    )

    assert stats["final_price"] == price[-1]
    assert stats["final_variance"] == variance[-1]
    assert stats["mean_price"] == np.mean(price)
    assert stats["mean_variance"] == np.mean(variance)


def test_cir_honours_the_requested_numerical_method():
    params = {"X0": 0.05, "kappa": 1.5, "theta": 0.05, "sigma": 0.3}
    _, euler = simulate_sde("cir", params, N=20, method="euler", seed=7, plot=False)
    _, milstein = simulate_sde("cir", params, N=20, method="milstein", seed=7, plot=False)

    assert not np.array_equal(euler, milstein)


def test_seed_makes_simulation_reproducible():
    params = {"S0": 100, "mu": 0.05, "sigma": 0.2}
    first = simulate_sde("gbm", params, N=10, seed=11, plot=False)
    second = simulate_sde("gbm", params, N=10, seed=11, plot=False)

    np.testing.assert_array_equal(first[1], second[1])
