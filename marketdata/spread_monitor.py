# cofure_bot/utils/spread_monitor.py

def detect_spread_condition(coin_data):
    alerts = []

    for coin in coin_data:
        spread = coin["spread"]

        if spread <= 0.8:
            alerts.append(f"📈 {coin['symbol']} có spread co mạnh → đang tích lũy")
        elif spread >= 1.3:
            alerts.append(f"⚠️ {coin['symbol']} có spread giãn cao → thị trường nhiễu")

    return alerts
