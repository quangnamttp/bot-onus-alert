import requests, json

def get_user_exchange(psid):
    try:
        with open("user_config.json") as f:
            config = json.load(f)
            return config.get(psid, {}).get("exchange", "onus")
    except: return "onus"

def get_price(psid):
    exchange = get_user_exchange(psid)
    if exchange == "onus":
        return get_onus_price("BTCUSDT")
    elif exchange == "nami":
        return get_nami_price("BTCUSDT")
    return 0

def get_onus_price(symbol):
    r = requests.get(f"https://api.goonus.io/v1/markets/{symbol}")
    try: return float(r.json()["data"]["price"])
    except: return 0

def get_nami_price(symbol):
    r = requests.get(f"https://api.nami.exchange/api/v1/ticker?symbol={symbol}")
    try: return float(r.json()["price"])
    except: return 0
