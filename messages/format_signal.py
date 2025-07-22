def format_signal_batch(signals):
    msg = "📊 Tín hiệu phiên hôm nay:\n"
    for sig in signals:
        emoji = "✅" if sig["strength"] >= 70 else "🟡" if sig["strength"] >= 50 else "⚠️"
        msg += f"\n{emoji} {sig['coin']} ({sig['type']})\n"
        msg += f"Entry: {sig['entry']} VNĐ\nTP: {sig['tp']} • SL: {sig['sl']}\n"
        msg += f"📋 Lý do: {sig['reason']}\n📈 Độ mạnh: {sig['strength']}%\n"
    return msg
