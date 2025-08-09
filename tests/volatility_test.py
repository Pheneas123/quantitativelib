from quantitativelib.volatility import analyse_volatility


analyse_volatility(
    ticker="AAPL",
    start_date="2016-01-01",
    end_date="2024-01-01",
    horizon=2,
    window=252,
    refit=21,
    dist="t",
    alphas=(0.01, 0.05),
    plot=True,
    plot_config={
        "figsize": (9, 4),
        "alpha_plot": 0.05,
        "style_var": {"lw": 1.2},
        "style_rv": {"lw": 1.0},
    },
    seed=1
)

#test 2

analyse_volatility(
    ticker="GOOGL",
    start_date="2018-01-01",
    end_date="2024-01-01",
    horizon=5,
    window=252,
    refit=21,
    dist="normal",
    alphas=(0.01, 0.05),
    plot=True,
    plot_config={
        "figsize": (10, 5),
        "alpha_plot": 0.1,
        "style_var": {"color": "green", "lw": 1.5},
        "style_rv": {"color": "orange", "lw": 1.0},
    },
    seed=2
)