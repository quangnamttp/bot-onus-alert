from marketdata.volume_scanner import get_surge_volume
from marketdata.spread_monitor import detect_spread_spike

def generate_emergency_signal():
    surges = get_surge_volume()
    spikes = detect_spread_spike()

    emergencies = []

    for coin in surges:
        if coin in spikes:
            v = surges[coin]
            s = spikes[coin]

            emergencies.append({
                "coin": coin,
                "entry": round(s['price'], -2),
                "reason": f"⏰ Volume bật mạnh {v['change']}%, funding lệch {v['bias']}, RSI vượt vùng {s['rsi']}",
                "advice": "Có thể cân nhắc vào lệnh sớm để đón đầu breakout.",
                "strength": "⚠️ KHẨN"
            })

    return emergencies
