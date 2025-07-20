def get_rsi(coin):
    sample_rsi = {
        "BTC": 46,
        "ETH": 53,
        "BNB": 51,
        "SOL": 28,
        "XRP": 49,
        "DOGE": 72,
        "SHIB": 65,
        "ADA": 37
    }
    return sample_rsi.get(coin.upper(), 50)
