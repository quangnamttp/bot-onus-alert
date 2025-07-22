from marketdata.volume_scanner import get_volume_data
from marketdata.spread_monitor import get_spread_data
from core.strength_classifier import classify_strength

def generate_signals():
    volume_info = get_volume_data()
    spread_info = get_spread_data()

    signals = []
    for coin in volume_info:
        if coin not in spread_info:
            continue

        v = volume_info[coin]
        s = spread_info[coin]

        strength = classify_strength(v, s)

        if strength >= 50:
            entry = round(s['price'], -2)
            signal = {
                "coin": coin,
                "entry": entry,
                "tp": entry + s['target_range'],
                "sl": entry - s['risk_range'],
                "type": "Limit",
                "strength": strength,
                "reason": f"Volume tăng {v['change']}%, funding nghiêng {s['bias']}, spread co."
            }
            signals.append(signal)

    return signals
