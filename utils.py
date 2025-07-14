def format_signal(signal):
    """
    Trả về chuỗi tin nhắn đẹp mắt cho tín hiệu giao dịch LONG hoặc SHORT.
    """
    emoji = "📈" if signal["type"] == "LONG" else "📉"
    volume_warn = "⚠️ Volume tăng mạnh!" if signal["volume_warn"] else ""
    
    return (
        f"{emoji} Tín hiệu {signal['type']} cho {signal['symbol']}\n"
        f"------------------------\n"
        f"🟡 Giá hiện tại: ${signal['price']:.6f}\n"
        f"📊 RSI: {signal['rsi']:.2f} | MA20: ${signal['ma20']:.6f}\n"
        f"🎯 TP: ${signal['tp']:.6f} | 🛡️ SL: ${signal['sl']:.6f}\n"
        f"💰 Volume: {signal['volume']:.2f}\n"
        f"{volume_warn}\n"
        f"📌 Kiểu lệnh: {signal['entry_type'].upper()}"
    )

def format_neutral(symbol, rsi, price, ma20):
    """
    Trả về giải thích khi chưa có điểm vào lệnh rõ ràng.
    """
    return (
        f"🤔 {symbol}: Chưa có tín hiệu vào lệnh.\n"
        f"▪ RSI hiện tại: {rsi:.2f} → chưa vào vùng mua/bán rõ\n"
        f"▪ Giá: ${price:.6f} chưa vượt MA20 (${ma20:.6f})\n"
        f"📌 Chờ thêm biến động mạnh hoặc tín hiệu volume để xác nhận điểm vào."
    )
