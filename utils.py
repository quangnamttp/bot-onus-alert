import datetime

def format_signal(signal):
    """
    Định dạng tín hiệu giao dịch kỹ thuật.
    Bao gồm cảnh báo volume, sát TP/SL, emoji, phân cấp độ mạnh/yếu.
    """

    # Biểu tượng loại lệnh
    type_icon = {
        "LONG": "🟢",
        "SHORT": "🔴",
        "NEUTRAL": "⚪"
    }.get(signal.get("type", "NEUTRAL"))

    # Cảnh báo sát TP hoặc SL (khoảng cách nhỏ hơn 1.5%)
    price = signal["price"]
    tp = signal["tp"]
    sl = signal["sl"]
    near_tp = abs(price - tp) / price < 0.015
    near_sl = abs(price - sl) / price < 0.015

    tp_sl_warn = ""
    if near_tp:
        tp_sl_warn = "📈 Giá đang tiến sát TP!"
    elif near_sl:
        tp_sl_warn = "⚠️ Giá tiến sát SL!"

    # Cảnh báo volume tăng
    volume_warn = ""
    if signal.get("volume_warn", False):
        volume_warn = "🚨 Volume tăng bất thường!"

    # Đánh giá độ mạnh
    trend_strength = "📡 Tín hiệu trung bình"
    rsi = signal["rsi"]
    if rsi < 20 or rsi > 80:
        trend_strength = "🔥 Tín hiệu mạnh!"
    elif rsi < 30 or rsi > 70:
        trend_strength = "⚡ Có tín hiệu đáng chú ý"

    # Thời gian phân tích (UTC+7)
    now = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

    # Tin nhắn tổng hợp
    text = (
        f"{type_icon} *{signal['type']}* tín hiệu cho {signal['symbol']}\n"
        f"📅 Thời điểm: {now}\n\n"
        f"💰 Giá vào lệnh: ${signal['price']:.6f}\n"
        f"🎯 TP: ${tp:.6f} | 📉 SL: ${sl:.6f}\n"
        f"📊 RSI: {rsi:.2f} | MA20: ${signal['ma20']:.6f}\n"
        f"🔍 Volume: {signal['volume']:.2f}\n"
        f"🚀 Lệnh: {signal['entry_type']}\n\n"
        f"{trend_strength}\n"
        f"{tp_sl_warn}\n"
        f"{volume_warn}"
    ).strip()

    return text
