import requests
from exchange_router import get_user_exchange

def get_price(symbol, psid):
    exchange = get_user_exchange(psid)
    if exchange == "onus":
        r = requests.get(f"https://api.goonus.io/v1/markets/{symbol}")
        return float(r.json()["data"]["price"])
    elif exchange == "nami":
        r = requests.get(f"https://api.nami.exchange/api/v1/ticker?symbol={symbol}")
        return float(r.json()["price"])
    return 0
