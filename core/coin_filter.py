# coin_filter.py

def is_valid_coin(coin):
    coin = coin.upper()
    blocked = ["BTCUP", "BTCDOWN", "ETH3L", "ETH3S", "DOGE5L", "SHIB1000"]
    if coin in blocked or not coin.isalnum():
        return False
    return True
