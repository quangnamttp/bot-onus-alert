import requests, json

def get_user_exchange(psid):
    try:
        with open("user_config.json") as f:
            config = json.load(f)
            return config.get(psid, {}).get("exchange", "onus")
    except: return "onus"

def get_price(psid, symbol="BTCUSDT"):
    exchange = get_user_exchange(psid)
    if exchange == "onus":
        return get_onus_price(symbol)
    elif exchange == "nami":
        return get_nami_price(symbol)
    return 0

def get_onus_price(symbol):
    try:
        r = requests.get(f"https://api.goonus.io/v1/markets/{symbol}")
        return float(r.json()["data"]["price"])
    except: return 0

def get_nami_price(symbol):
    try:
        r = requests.get(f"https://api.nami.exchange/api/v1/ticker?symbol={symbol}")
        return float(r.json()["price"])
    except: return 0
