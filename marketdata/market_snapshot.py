# market_snapshot.py

from marketdata.price_fetcher import fetch_price

def get_market_snapshot(coins):
    """
    Trả về bảng giá của danh sách coin hiện tại
    """
    snapshot = []
    for coin in coins:
        price = fetch_price(coin)
        if price:
            snapshot.append(f"💹 {coin.upper()}: {price}$")
    return snapshot
