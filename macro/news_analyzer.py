# macro/news_analyzer.py

def analyze_post_news(market_data):
    """
    Phân tích phản ứng thị trường sau tin vĩ mô dựa trên chỉ số thị trường
    """

    funding = market_data.get("funding", 0)
    volume  = market_data.get("volume", 0)
    rsi     = market_data.get("rsi", 50)
    spread  = market_data.get("spread", 1.5)

    signals = []

    if funding > 0.008 and volume > 30 and rsi > 55 and spread < 1.2:
        signals.append("✅ Thị trường phản ứng tích cực mạnh → có thể cân nhắc Long")
    elif funding < -0.008 and rsi < 45 and spread > 1.3:
        signals.append("🔴 Phản ứng tiêu cực → nên đứng ngoài để tránh nhiễu")
    elif volume > 35 and spread < 1.1:
        signals.append("💡 Volume mạnh, spread ổn định → có thể canh breakout nếu giá xác nhận")
    elif funding > 0.006 and volume < 20:
        signals.append("🤔 Tâm lý tốt nhưng lực giao dịch yếu → cần chờ thêm xác nhận")
    else:
        signals.append("⚠️ Dữ liệu chưa rõ ràng → nên theo dõi thêm trước khi vào lệnh")

    return signals
