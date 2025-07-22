def format_emergency_signals(emergencies):
    if not emergencies:
        return "✅ Không có tín hiệu khẩn nào được phát hiện lúc này."

    msg = "⏰ Tín hiệu khẩn phát hiện:\n"
    for e in emergencies:
        msg += f"\n🚨 {e['coin']} → Entry: {e['entry']} VNĐ\n"
        msg += f"{e['reason']}\n{e['advice']}\n"
    return msg
