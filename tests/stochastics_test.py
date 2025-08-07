from quantitativelib.stochastics import simulate_sde

# Example 1
simulate_sde("gbm", params={"S0": 100, "mu": 0.05, "sigma": 0.2}, seed=0, plot=False)

# Example 2
simulate_sde("cir", params={"X0": 0.05, "kappa": 1.5, "theta": 0.05, "sigma": 0.1}, seed=1, plot=False)

# Example 3
simulate_sde("ou", params={"X0": 0.0, "mu": 0.7, "theta": 1.0, "sigma": 0.3}, seed=2, plot=False)

# Example 4
simulate_sde(
    "heston",
    params={"S0": 100, "V0": 0.04, "mu": 0.05, "kappa": 1.5, "theta": 0.04, "xi": 0.3, "rho": -0.7},
    seed=3,
    plot=True,
    plot_config={
        "which": "both",
        "figsize": (12, 6),
        "title": "Heston Model: Price and Variance",
        "S": {"label": "Asset Price", "color": "blue", "linewidth": 1.5},
        "V": {"label": "Variance", "color": "red", "linewidth": 1.5},
    }
)

# Example 5
simulate_sde("merton", params={"S0": 100, "mu": 0.1, "sigma": 0.2, "lambd": 0.5, "m": -0.1, "v": 0.02}, seed=4, plot=False)