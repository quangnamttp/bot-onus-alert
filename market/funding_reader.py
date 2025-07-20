def get_funding(coin):
    sample_funding = {
        "BTC": 0.006,
        "ETH": 0.002,
        "BNB": -0.008,
        "SOL": -0.012,
        "XRP": 0.004,
        "DOGE": 0.018,
        "SHIB": 0.022,
        "ADA": -0.016
    }
    return sample_funding.get(coin.upper(), 0.0)
