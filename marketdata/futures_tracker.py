# cofure_bot/marketdata/futures_tracker.py

import requests

def get_futures_data():
    try:
        response = requests.get("https://api.onus.io/futures-market")
        data = response.json()

        coins = []
        for item in data.get("symbols", []):
            coins.append({
                "symbol": item["symbol"],
                "price": item["lastPrice"],
                "funding": item["fundingRate"],
                "volume_change": item["volumeChange"],
                "rsi": item["rsi"],
                "spread": item["spread"]
            })

        return coins
    except:
        return []

def get_price_data():
    try:
        response = requests.get("https://api.onus.io/futures-market")
        data = response.json()
        result = {}

        for coin in data.get("symbols", []):
            if coin["symbol"] in ["BTC", "ETH", "SOL"]:
                result[coin["symbol"]] = coin["lastPrice"]

        return result
    except:
        return {"BTC": 0, "ETH": 0, "SOL": 0}
