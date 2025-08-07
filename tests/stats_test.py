from quantitativelib.stats import analyse


# Example usage of the `analyse` function
analyse(
    ticker=["AAPL", "MSFT", "GOOGL"],
    start_date="2021-01-01",
    end_date="2023-01-01",  
    overlay_price=True,
    stats=["mean", "sharpe", "cumulative"],
    round_decimals=3,
    plot_kwargs={"grid": True},
)