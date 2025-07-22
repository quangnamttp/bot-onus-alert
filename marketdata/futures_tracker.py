def get_top_coin_data():
    # Mô phỏng lấy funding & giá top coin — thay bằng API thật nếu có
    return {
        "BTC": { "funding": "+0.03%", "price": 183_200_000 },
        "ETH": { "funding": "-0.01%", "price": 56_700_000 },
        "SOL": { "funding": "+0.04%", "price": 3_750_000 }
    }

def get_all_futures():
    # Trả về danh sách toàn bộ coin Futures đang được ONUS hỗ trợ
    return ["BTC", "ETH", "SOL", "NEO", "CHI", "C98", "MATIC", "DOGE"]
