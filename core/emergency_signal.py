# cofure_bot/core/emergency_signal.py

import time
from marketdata.futures_tracker import get_futures_data
from strength_classifier import classify_strength
from messenger.send_message import send_message
from messages.emergency_format import format_emergency_signal
from utils.config_loader import MY_USER_ID

def detect_emergency_conditions(coin_data):
    signals = []
    for coin in coin_data:
        fund = coin["funding"]
        vol = coin["volume_change"]
        rsi = coin["rsi"]
        spread = coin["spread"]
        price = coin["price"]

        if fund >= 0.006 and vol >= 25 and rsi >= 55 and spread <= 0.8:
            direction = "Long"
        elif fund <= -0.006 and vol >= 25 and rsi <= 42 and spread >= 1.3:
            direction = "Short"
        else:
            continue

        strength, label = classify_strength(fund, vol, rsi, spread)
        signals.append({
            "coin": coin["symbol"],
            "entry": price,
            "tp": price * 1.07 if direction == "Long" else price * 0.93,
            "sl": price * 0.95 if direction == "Long" else price * 1.05,
            "funding": fund,
            "volume": vol,
            "rsi": rsi,
            "spread": spread,
            "strength": strength,
            "strength_label": label,
            "direction": direction,
            "order_type": "Market"
        })
    return signals

def send_emergency_signal(signal):
    message = format_emergency_signal(signal)
    send_message(MY_USER_ID, message)

def run_emergency_monitor():
    coin_data = get_futures_data()  # Lấy dữ liệu ONUS Futures realtime
    alerts = detect_emergency_conditions(coin_data)
    for signal in alerts:
        send_emergency_signal(signal)

