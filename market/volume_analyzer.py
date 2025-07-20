def get_volume(coin):
    sample_volumes = {
        "BTC": 520_000,
        "ETH": 330_000,
        "BNB": 240_000,
        "SOL": 180_000,
        "XRP": 160_000,
        "DOGE": 90_000,
        "SHIB": 80_000,
        "ADA": 105_000
    }
    return sample_volumes.get(coin.upper(), 100_000)
