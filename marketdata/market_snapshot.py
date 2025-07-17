def get_market_data():
    # ⚠️ Giả lập — sau này gọi từ API hoặc file cache
    return [
        {
            "symbol": "BTCUSDT",
            "price": 1548000000,
            "volume": 300000,
            "rsi": 48,
            "funding": -0.008,
            "change": 3.7
        },
        {
            "symbol": "ETHUSDT",
            "price": 90500000,
            "volume": 180000,
            "rsi": 52,
            "funding": 0.015,
            "change": 2.3
        }
    ]
