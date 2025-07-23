from utils.vnđ_formatter import format as format_vnd

def format_signal_batch(signals):
    msg = "📊 Tín hiệu phiên hôm nay:\n"
    for idx, sig in enumerate(signals, 1):
        emoji = "✅" if sig["strength"] >= 70 else "🟡" if sig["strength"] >= 50 else "⚠️"
        entry = format_vnd(sig["entry"])
        tp = format_vnd(sig["tp"])
        sl = format_vnd(sig["sl"])
        nhan = " — Tham khảo" if sig["strength"] < 50 else ""

        msg += f"\n{emoji} [{idx}] {sig['coin']} ({sig.get('type', 'Long')}){nhan}\n"
        msg += f"📌 Chiến lược: {sig.get('strategy', 'Scalping')} • Lệnh: {sig.get('order_type', 'Market')}\n"
        msg += f"💰 Entry: {entry}\n🎯 TP: {tp} • 🛡️ SL: {sl}\n"
        msg += f"📋 Lý do: {sig['reason']}\n📈 Độ mạnh: {sig['strength']}%\n"
    return msg
