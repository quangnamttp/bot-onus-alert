# cofure_bot/core/signal_generator.py

from marketdata.futures_tracker import get_futures_data
from core.strength_classifier import classify_strength
from core.pre_breakout_detector import detect_pattern

def generate_signals():
    coin_data = get_futures_data()
    signals = []

    for coin in coin_data:
        fund = coin["funding"]
        vol = coin["volume_change"]
        rsi = coin["rsi"]
        spread = coin["spread"]
        price = coin["price"]
        pattern = detect_pattern(coin["symbol"])
        
        strength, label = classify_strength(fund, vol, rsi, spread)

        direction = None
        if fund > 0.005 and rsi > 54 and pattern in ["tam giác tăng", "nền phẳng"]:
            direction = "Long"
        elif fund < -0.005 and rsi < 45 and pattern in ["vai đầu vai", "nền giảm"]:
            direction = "Short"
        else:
            continue

        signals.append({
            "symbol": coin["symbol"],
            "order_type": "Market",
            "strategy": "Scalping" if len(signals) < 3 else "Swing",
            "side": direction,
            "entry": price,
            "tp": price * 1.07 if direction == "Long" else price * 0.93,
            "sl": price * 0.95 if direction == "Long" else price * 1.05,
            "funding": fund,
            "volume_change": vol,
            "rsi": rsi,
            "spread": spread,
            "pattern": pattern,
            "strength": strength,
            "strength_label": label,
            "session_time": "Real-time"
        })

        if len(signals) == 5:
            break

    return signals
