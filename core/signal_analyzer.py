# signal_analyzer.py

import random

class SignalAnalyzer:
    def __init__(self, coin, exchange):
        self.coin = coin.upper()
        self.exchange = exchange
        self.data = {}  # giả lập dữ liệu

    def fetch_indicators(self):
        # Dữ liệu mô phỏng
        self.data = {
            "RSI": random.randint(30, 80),
            "MA": "trên MA20" if random.choice([True, False]) else "dưới MA20",
            "Volume": random.randint(500_000, 4_000_000)
        }
        return self.data

    def format_analysis(self):
        indicators = self.fetch_indicators()
        return (
            f"→ RSI: {indicators['RSI']} | MA: Giá đang {indicators['MA']}\n"
            f"→ Volume hiện tại: {indicators['Volume']:,} USDT"
        )
