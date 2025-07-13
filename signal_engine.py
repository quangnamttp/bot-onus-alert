import requests
import pandas as pd
import ta

BINANCE_API = "https://api.binance.com"

# ==== LẤY DỮ LIỆU NẾN TỪ BINANCE ====
def fetch_klines(symbol, interval="15m", limit=100):
    url = f"{BINANCE_API}/api/v3/klines?symbol={symbol.upper()}USDT&interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades", "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        return df
    return None

# ==== PHÁT HIỆN COIN CÓ TÍN HIỆU VÀO LỆNH ====
def scan_entry():
    coin_list = ["BTC", "ETH", "SOL", "SHIB", "PEPE", "XRP", "SUI", "MOG", "APU"]  # Có thể mở rộng
    for symbol in coin_list:
        df = fetch_klines(symbol)
        if df is not None:
            # Tính RSI và MA20
            df["rsi"] = ta.momentum.RSIIndicator(close=df["close"]).rsi()
            df["ma20"] = ta.trend.SMAIndicator(close=df["close"], window=20).sma_indicator()
            latest_rsi = df["rsi"].iloc[-1]
            latest_price = df["close"].iloc[-1]
            latest_ma = df["ma20"].iloc[-1]
            latest_volume = df["volume"].iloc[-1]

            # Điều kiện tín hiệu vào lệnh: RSI thấp + giá vượt MA + volume cao
            if latest_rsi < 35 and latest_price > latest_ma and latest_volume > df["volume"].mean():
                return {
                    "symbol": symbol,
                    "entry": round(latest_price, 4),
                    "rsi": round(latest_rsi, 2),
                    "ma": round(latest_ma, 4),
                    "volume": round(latest_volume, 2)
                }
    return None
