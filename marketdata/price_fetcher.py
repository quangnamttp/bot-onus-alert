# marketdata/price_fetcher.py

def fetch_price(coin, exchange):
    prices = {
        "Onus": {"SOL": 149.80, "BTC": 59200, "ETH": 3400},
        "Binance": {"SOL": 149.50, "BTC": 59050, "ETH": 3390},
        "OKX": {"SOL": 150.10, "BTC": 59120, "ETH": 3405},
        "MEXC": {"SOL": 149.90, "BTC": 59220, "ETH": 3410},
        "Bybit": {"SOL": 148.90, "BTC": 58980, "ETH": 3380},
        "Nami": {"SOL": 149.60, "BTC": 59100, "ETH": 3395}
    }

    coin = coin.upper()
    exchange = exchange.title()
    price = prices.get(exchange, {}).get(coin, None)
    if price:
        price_vnd = round(price * 24350, 0)
        return f"${price} ≈ {price_vnd:,} VNĐ (sàn {exchange})"
    return f"❌ Không tìm thấy giá của {coin} trên sàn {exchange}"
