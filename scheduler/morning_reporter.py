from mess_handler import send_message

def send_morning_news():
    msg = (
        "🌞 Chào buổi sáng đội ngũ Futures!\n"
        "📈 Tỷ giá USDT/VND: 25,100 (giá xử lý gốc)\n"
        "🧠 BTC hồi nhẹ, funding âm đầu phiên\n"
        "📊 Lịch tin hôm nay: CPI 19h30, FOMC 22h00\n"
        "✨ Chúc team khởi đầu ngày mới đầy năng lượng nha!"
    )
    send_message(msg)
