# market_data.py
import requests

BASE_URL = "https://api.binance.com/api/v3"

def get_all_symbols():
    """Lấy danh sách tất cả cặp USDT đang giao dịch"""
    res = requests.get(f"{BASE_URL}/ticker/price").json()
    return [s["symbol"] for s in res if s["symbol"].endswith("USDT")]

def get_price(symbol):
    """Lấy giá hiện tại của 1 đồng coin (ví dụ BTCUSDT)"""
    res = requests.get(f"{BASE_URL}/ticker/price?symbol={symbol}").json()
    return float(res["price"])

def get_volume(symbol):
    """Lấy volume 24h của đồng coin"""
    res = requests.get(f"{BASE_URL}/ticker/24hr?symbol={symbol}").json()
    return float(res["quoteVolume"])

def get_kline(symbol, interval="15m", limit=100):
    """Lấy dữ liệu nến cho phân tích kỹ thuật"""
    url = f"{BASE_URL}/klines?symbol={symbol}&interval={interval}&limit={limit}"
    res = requests.get(url).json()
    return res  # dạng [timestamp, open, high, low, close, volume, ...]

def get_rsi(data, period=14):
    """Tính RSI dựa trên dữ liệu nến"""
    import numpy as np
    closes = np.array([float(k[4]) for k in data])
    deltas = np.diff(closes)
    up = deltas[deltas > 0].sum() / period
    down = abs(deltas[deltas < 0].sum()) / period
    rs = up / down if down != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

