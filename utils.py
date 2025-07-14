def format_signal(signal):
    type_emoji = {
        "LONG": "📈 MUA (LONG)",
        "SHORT": "📉 BÁN (SHORT)",
        "NEUTRAL": "⏸️ TRUNG LẬP"
    }

    direction = type_emoji.get(signal["type"], "❓")
    symbol = signal["symbol"]
    price = f"${signal['price']:.6f}"
    rsi = f"{signal['rsi']:.2f}"
    ma20 = f"${signal['ma20']:.6f}"
    tp = f"${signal['tp']:.6f}"
    sl = f"${signal['sl']:.6f}"
    volume = f"{signal['volume']:.2f}"
    warning = "⚠️ Volume tăng bất thường!" if signal["volume_warn"] else ""

    entry_note = f"📌 Lệnh thị trường: {signal['entry_type'].upper()}"
    tp_sl_note = f"🎯 TP: {tp}\n🛡️ SL: {sl}"

    message = (
        f"{direction} cho {symbol}\n"
        f"------------------------\n"
        f"🟡 Giá hiện tại: {price}\n"
        f"📊 RSI: {rsi} | MA20: {ma20}\n"
        f"💰 Khối lượng: {volume}\n"
        f"{tp_sl_note}\n"
        f"{entry_note}\n"
        f"{warning}"
    )
    return message
