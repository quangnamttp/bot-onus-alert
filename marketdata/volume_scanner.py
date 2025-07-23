# cofure_bot/utils/volume_scanner.py

def scan_high_volume(coin_data, threshold=25):
    strong_volume_coins = []

    for coin in coin_data:
        if coin["volume_change"] >= threshold:
            strong_volume_coins.append({
                "symbol": coin["symbol"],
                "volume_change": coin["volume_change"]
            })

    return strong_volume_coins
