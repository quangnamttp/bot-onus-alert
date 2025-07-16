# rsi_calculator.py

import pandas as pd

def calculate_rsi(prices, period=14):
    """
    Tính RSI từ danh sách giá đóng cửa
    """
    df = pd.DataFrame(prices, columns=["close"])
    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return round(rsi.iloc[-1], 2)
