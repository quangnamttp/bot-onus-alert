# cofure_bot/messages/emergency_format.py

from utils.vnd_formatter import format_vnd

def format_emergency_signal(s):
    entry = format_vnd(s["entry"])
    tp = format_vnd(s["tp"])
    sl = format_vnd(s["sl"])
    emoji = "✅" if s["strength"] >= 85 else "🟡"

    action = "MUA" if s["direction"] == "Long" else "BÁN"

    return f"""
🔴 Tín hiệu khẩn — {s['coin']} ({s['direction']})

📌 Lệnh: {s['order_type']} • Thời điểm: realtime  
➡️ Hành động: {action} ngay tại {entry}

🎯 TP: {tp} • 🛡️ SL: {sl}

📋 Phân tích kỹ thuật:
• Funding: {s['funding']} • Volume: +{s['volume']}%  
• RSI: {s['rsi']} • Spread: {s['spread']}

📈 Độ mạnh tín hiệu: {emoji} {s['strength']}% — {s['strength_label']}  
⏰ Dự báo breakout → nên vào sớm để đón trend 📬
""".strip()
