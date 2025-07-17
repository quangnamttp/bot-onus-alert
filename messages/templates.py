def format_signal(signal):
    emoji = "📍" if signal.get("note") == "📌 Tham khảo" else "🚀"
    return (
        f"{emoji} {signal['symbol']} | {signal['strategy']}\n"
        f"💰 Entry: {signal['entry']:,} VND\n"
        f"🛡 SL: {signal['sl']:,} | 🎯 TP: {signal['tp']:,}\n"
        f"⚖️ R:R: {signal['rr']} | {signal.get('note', '✅ Ready')}"
    )

def format_macro_warning(event):
    return (
        f"🔔 Tin vĩ mô: {event['time']} — {event['title']}\n"
        f"⚡ Độ quan trọng: {event['impact']}\n"
        f"📌 Gợi ý: Quản lý SL hợp lý, tránh vào lệnh lúc biến động!"
    )
