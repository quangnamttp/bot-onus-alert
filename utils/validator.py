# validator.py

def is_valid_coin(coin):
    coin = coin.upper()
    blocked = ["BTCUP", "BTCDOWN", "ETH3L", "ETH3S", "SHIB1000"]
    return coin.isalnum() and coin not in blocked

def is_valid_exchange(exchange):
    valid = ["Binance", "OKX", "MEXC", "Nami", "Onus", "Bybit"]
    return exchange.capitalize() in valid
