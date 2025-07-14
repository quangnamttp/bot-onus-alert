# utils.py
def format_price(p):
    """Làm tròn giá và chuẩn hoá hiển thị"""
    return f"${round(float(p), 6)}"

def emoji_signal(type_):
    """Emoji phù hợp với loại tín hiệu"""
    return "🟢" if type_ == "LONG" else "🔴"

def format_signal(sig):
    """Xây dựng tin nhắn văn bản gửi người dùng"""
    emoji = emoji_signal(sig["type"])
    symbol = sig["symbol"].replace("USDT", "")
    msg = (
        f"{emoji} Tín hiệu {sig['type']} {symbol}/USDT\n"
        f"💰 Giá hiện tại: {format_price(sig['price'])}\n"
        f"📈 RSI: {sig['rsi']} | MA20: {format_price(sig['ma20'])}\n"
        f"📊 Volume: {sig['volume']}\n"
        f"📌 Loại lệnh: {sig['entry_type']}\n"
        f"🎯 TP: {format_price(sig['tp'])} | 🛑 SL: {format_price(sig['sl'])}"
    )
    return msg

def format_time(seconds):
    """Định dạng thời gian chờ chu kỳ (ví dụ: 15 phút)"""
    m, s = divmod(seconds, 60)
    return f"{m}m{s}s"

def is_valid_signal(sig):
    """Kiểm tra xem tín hiệu có hợp lệ để gửi hay không"""
    return sig["rsi"] > 0 and sig["volume"] > 0
