import requests

BINANCE_URL = "https://api.binance.com"

# ✅ Kiểm tra token có tồn tại trên Binance
def check_symbol_exists(symbol):
    try:
        res = requests.get(f"{BINANCE_URL}/api/v3/exchangeInfo", timeout=5)
        data = res.json()
        available = [s["symbol"] for s in data["symbols"] if s["status"] == "TRADING"]
        return symbol.upper() in available
    except Exception as e:
        print(f"⛔ Lỗi check_symbol_exists: {e}")
        return False

# ✅ Lấy dữ liệu nến (K-line)
def get_kline(symbol, interval="1h", limit=100):
    try:
        url = f"{BINANCE_URL}/api/v3/klines"
        params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
        res = requests.get(url, params=params, timeout=5)
        return res.json()
    except Exception as e:
        print(f"⛔ Lỗi get_kline: {e}")
        return []

# ✅ Tính RSI (Relative Strength Index)
def get_rsi(candles, period=14):
    try:
        closes = [float(k[4]) for k in candles]  # Lấy giá đóng cửa
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
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    except Exception as e:
        print(f"⛔ Lỗi get_rsi: {e}")
        return 50.0

# ✅ Lấy giá hiện tại của token
def get_price(symbol):
    try:
        url = f"{BINANCE_URL}/api/v3/ticker/price"
        res = requests.get(url, params={"symbol": symbol.upper()}, timeout=5)
        return float(res.json()["price"])
    except Exception as e:
        print(f"⛔ Lỗi get_price: {e}")
        return 0.0

# ✅ Lấy volume từ cây nến gần nhất
def get_volume(symbol):
    try:
        candles = get_kline(symbol, interval="1h", limit=2)
        latest = candles[-1]
        return float(latest[5])  # Khối lượng giao dịch
    except Exception as e:
        print(f"⛔ Lỗi get_volume: {e}")
        return 0.0

# ✅ Lấy toàn bộ symbol có giao dịch USDT
def get_all_symbols():
    try:
        url = f"{BINANCE_URL}/api/v3/exchangeInfo"
        res = requests.get(url, timeout=5)
        data = res.json()
        symbols = [
            s["symbol"]
            for s in data["symbols"]
            if s["symbol"].endswith("USDT") and s["status"] == "TRADING"
        ]
        return symbols
    except Exception as e:
        print(f"⛔ Lỗi get_all_symbols: {e}")
        return []
