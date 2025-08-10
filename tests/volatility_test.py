from quantitativelib.volatility import analyse_volatility



# Test configuration
analyse_volatility(
    ticker="AAPL", start_date="2020-01-01", end_date="2023-12-31",
    horizon=1, window=500, refit=50, dist="t",
    plot=True,
    plot_modes=("var_vs_r2", "var_vs_realised_var_roll"),
    roll_window=21
)

# Vol forecast vs rolling realised vol + cumulative VaR hits (for 5%)
analyse_volatility(
    ticker="AAPL", start_date="2020-01-01", end_date="2023-12-31",
    horizon=1, window=500, refit=50, dist="t", alphas=(0.01, 0.05),
    plot=True,
    plot_modes=("vol_vs_realised_vol_roll", "var_hits_cum"),
    roll_window=21,
    alpha_plot=0.05
)