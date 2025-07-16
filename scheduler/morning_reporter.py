def morning_brief(coin, exchange):
    mood = "tăng nhẹ do tín hiệu hồi phục" if coin.lower() in ["btc", "eth", "sol"] else "giảm do áp lực bán"
    return (
        f"🌅 Chào buổi sáng!\n"
        f"Sàn: {exchange} | Coin: {coin.upper()}\n\n"
        f"📊 Dự báo: Thị trường hôm nay có thể {mood}\n"
        "⚠️ Theo dõi lịch kinh tế lúc 07:00\n"
        "🎯 Ưu tiên Scalp khung M15 nếu volume ổn định"
    )
