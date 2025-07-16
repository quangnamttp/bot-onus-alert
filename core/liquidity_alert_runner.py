# liquidity_alert_runner.py

from marketdata.liquidity_detector import detect_liquidity_spike

def check_liquidity_batch(coins):
    alerts = []
    for coin in coins:
        alert = detect_liquidity_spike(coin)
        if alert:
            alerts.append(alert)
    return alerts
