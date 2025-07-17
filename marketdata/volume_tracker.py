def track_volume(data):
    results = {}
    for coin in data:
        symbol = coin["symbol"]
        volume = coin["volume"]
        results[symbol] = volume
    return results
