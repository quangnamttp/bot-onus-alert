# morning_reporter.py

def morning_brief(coin, exchange):
    mood = "Tăng nhẹ do tín hiệu hồi phục từ thị trường Mỹ" if coin.lower() in ["btc", "eth", "sol"] else "Giảm nhẹ do áp lực bán từ phiên Á"
    return (
        f"🌅 Chào buổi sáng trader!\n"
        f"📍 Sàn: {exchange} | Coin: {coin.upper()}\n\n"
        f"📊 Dự báo: Thị trường hôm nay có khả năng {mood}\n"
        f"📌 Lưu ý: Theo dõi lịch kinh tế & dòng tiền bất thường\n"
        f"🧠 Chiến lược gợi ý: Ưu tiên Scalp khung ngắn (M15–H1)"
    )
