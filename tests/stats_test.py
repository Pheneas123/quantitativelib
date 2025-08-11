from quantitativelib.stats import analyse, risk_metrics
import pandas as pd

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

# Example usage of the `risk_metrics` function
risk_metrics_example = pd.DataFrame(risk_metrics(
    ticker="AAPL",
    start_date="2021-01-01",
    end_date="2023-01-01",
    risk_free_rate=0.01,
    alpha=0.05,
    force_positive=True
))

print(risk_metrics_example)

