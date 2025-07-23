# cofure_bot/messages/format_signal.py

from utils.vnd_formatter import format_vnd

def format_signal_batch(signals):
    parts = ["📊 Dưới đây là 5 tín hiệu phiên Cofure — gồm 3 Scalping + 2 Swing:\n"]
    
    for idx, s in enumerate(signals, start=1):
        entry = format_vnd(s["entry"])
        tp = format_vnd(s["tp"])
        sl = format_vnd(s["sl"])
        strength = s["strength"]
        emoji = "✅" if strength >= 70 else "🟡" if strength >= 50 else "⚠️"

        text = f"""
{emoji} Signal #{idx} — {s['symbol']} ({s['strategy']} • {s['side']})

📌 Lệnh: {s['order_type']} • Phiên: {s['session_time']}  
➡️ Hành động: {'MUA' if s['side'] == 'Long' else 'BÁN'} ngay tại {entry}

🎯 TP: {tp} • 🛡️ SL: {sl}

📋 Lý do kỹ thuật:
• Funding: {s['funding']} • Volume: +{s['volume_change']}%  
• RSI: {s['rsi']} • Spread: {s['spread']}  
• Mô hình: {s['pattern']}  

📈 Độ mạnh: {emoji} {strength}% — {s['strength_label']}
"""
        parts.append(text.strip())

    return "\n\n".join(parts)
