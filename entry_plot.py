import requests
import pandas as pd
import matplotlib.pyplot as plt
import ta
from io import BytesIO
from PIL import Image

BINANCE_API = "https://api.binance.com"

# ==== LẤY DỮ LIỆU NẾN ====
def fetch_klines(symbol, interval="15m", limit=100):
    url = f"{BINANCE_API}/api/v3/klines?symbol={symbol.upper()}USDT&interval={interval}&limit={limit}"
    res = requests.get(url).json()
    df = pd.DataFrame(res, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades", "taker_base", "taker_quote", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    return df

# ==== VẼ BIỂU ĐỒ ENTRY ====
def plot_entry(symbol):
    df = fetch_klines(symbol)
    df["ma20"] = ta.trend.SMAIndicator(df["close"], window=20).sma_indicator()

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["close"], label="Giá Close", color="cyan", linewidth=2)
    ax.plot(df["ma20"], label="MA20", color="orange", linestyle="--")

    ax.set_title(f"Biểu đồ {symbol.upper()} — Khung 15 phút", fontsize=16)
    ax.set_xlabel("Nến gần nhất")
    ax.set_ylabel("Giá (USDT)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Xuất ảnh ra buffer
    buf = BytesIO()
    plt.savefig(buf, format="PNG", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    image = Image.open(buf)
    return image
