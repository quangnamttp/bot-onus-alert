def format_signal(signal):
    """
    Định dạng tín hiệu kỹ thuật thành tin nhắn hiển thị đẹp
    Input: dict signal chứa các thông số kỹ thuật
    Output: chuỗi văn bản sẵn sàng để gửi qua Messenger
    """

    # Biểu tượng theo loại tín hiệu
    type_emoji = {
        "LONG": "🟢",
        "SHORT": "🔴",
        "NEUTRAL": "⚪"
    }.get(signal.get("type", "NEUTRAL"))

    # Format nội dung
    message = (
        f"{type_emoji} *{signal['type']}* tín hiệu cho {signal['symbol']}\n\n"
        f"💰 Giá vào lệnh: ${signal['price']:.6f}\n"
        f"🎯 TP: ${signal['tp']:.6f} | 📉 SL: ${signal['sl']:.6f}\n"
        f"📊 RSI: {signal['rsi']:.2f} | MA20: ${signal['ma20']:.6f}\n"
        f"🔍 Volume: {signal['volume']:.2f}\n"
        f"🚀 Lệnh: {signal['entry_type']}"
    )

    return message
