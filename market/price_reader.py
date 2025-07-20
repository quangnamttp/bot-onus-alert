def get_price(coin):
    # Giá giả lập — bạn có thể thay bằng API bên ngoài
    sample_prices = {
        "BTC": 982_000_000,
        "ETH": 68_500_000,
        "BNB": 15_250_000,
        "SOL": 1_960_000,
        "XRP": 13_500,
        "DOGE": 4_200,
        "SHIB": 0.38,
        "ADA": 9_800
    }
    return sample_prices.get(coin.upper(), 100_000)
