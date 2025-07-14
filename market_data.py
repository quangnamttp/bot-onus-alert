import requests

BINANCE_URL = "https://api.binance.com"

def get_all_symbols():
    try:
        url = f"{BINANCE_URL}/api/v3/exchangeInfo"
        res = requests.get(url, timeout=5)
        data = res.json()
        return [
            s["symbol"]
            for s in data["symbols"]
            if s["symbol"].endswith("USDT") and s["status"] == "TRADING"
        ]
    except Exception as e:
        print(f"⛔ get_all_symbols error: {e}")
        return []

def get_kline(symbol, interval="1h", limit=100):
    try:
        url = f"{BINANCE_URL}/api/v3/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        res = requests.get(url, params=params, timeout=5)
        return res.json()
    except Exception as e:
        print(f"⛔ get_kline error: {e}")
        return []

def get_rsi(candles, period=14):
    try:
        closes = [float(k[4]) for k in candles]
        gains, losses = [], []
        for i in range(1, len(closes)):
            delta = closes[i] - closes[i - 1]
            gains.append(max(delta, 0))
            losses.append(max(-delta, 0))
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)
    except Exception as e:
        print(f"⛔ get_rsi error: {e}")
        return 50.0

def get_price(symbol):
    try:
        url = f"{BINANCE_URL}/api/v3/ticker/price"
        res = requests.get(url, params={"symbol": symbol}, timeout=5)
        return float(res.json()["price"])
    except Exception as e:
        print(f"⛔ get_price error: {e}")
        return 0.0

def get_volume(symbol):
    try:
        candles = get_kline(symbol, interval="1h", limit=2)
        return float(candles[-1][5])
    except Exception as e:
        print(f"⛔ get_volume error: {e}")
        return 0.0

def get_trending_tokens(top=5):
    try:
        symbols = get_all_symbols()
        trending = []
        for symbol in symbols[:200]:
            candles = get_kline(symbol, limit=2)
            if not candles: continue
            vol_now = float(candles[-1][5])
            vol_prev = float(candles[-2][5])
            if vol_prev == 0: continue
            rate = vol_now / vol_prev
            trending.append((symbol, rate))
        trending.sort(key=lambda x: x[1], reverse=True)
        return trending[:top]
    except Exception as e:
        print(f"⛔ get_trending_tokens error: {e}")
        return []
