# entry_plot.py
import matplotlib.pyplot as plt
import numpy as np
import os

def draw_entry_chart(candles, symbol, entry_price, tp=None, sl=None, save_path="entry_chart.png"):
    """Vẽ biểu đồ giá + MA20 + điểm vào, TP, SL"""
    closes = [float(k[4]) for k in candles]
    times = [k[0] for k in candles]
    ma20 = np.convolve(closes, np.ones(20)/20, mode='valid')

    plt.figure(figsize=(10, 5))
    plt.plot(closes, label="Giá đóng cửa", color="blue")
    plt.plot(range(19, len(closes)), ma20, label="MA20", color="orange")
    plt.axhline(entry_price, color="green", linestyle="--", label=f"Entry: {entry_price}")

    if tp:
        plt.axhline(tp, color="lime", linestyle=":", label=f"TP: {tp}")
    if sl:
        plt.axhline(sl, color="red", linestyle=":", label=f"SL: {sl}")

    plt.title(f"{symbol} Entry Chart")
    plt.xlabel("Nến 15m gần đây")
    plt.ylabel("Giá")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path
