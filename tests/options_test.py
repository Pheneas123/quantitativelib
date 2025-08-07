from quantitativelib.options import black_scholes

# Example usage of the `black_scholes` function
option_prices = black_scholes(
    option_type=['call', 'put'],
    K=150,
    S=145,
    T=1,
    r=0.01,  
    q=0.02,  
    sigma=0.2,  
    precision=4,
    show_table=True
)