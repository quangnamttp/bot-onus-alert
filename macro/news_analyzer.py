# macro/news_analyzer.py

def analyze_post_news(market_data, news_context=None):
    """
    Phân tích phản ứng thị trường sau tin vĩ mô dựa trên chỉ số kỹ thuật + bối cảnh tin tức

    market_data: dict → gồm funding, volume, rsi, spread
    news_context: dict tùy chọn → gồm impact, event_type, timestamp, v.v.
    """

    # 🔧 Lấy dữ liệu thị trường (với giá trị mặc định nếu thiếu)
    funding = market_data.get("funding", 0)
    volume  = market_data.get("volume", 0)
    rsi     = market_data.get("rsi", 50)
    spread  = market_data.get("spread", 1.5)

    # 🔍 Ngữ cảnh tin tức nếu có
    impact     = news_context.get("impact", "medium").lower() if news_context else "medium"
    event_type = news_context.get("event_type", "").lower() if news_context else ""

    signals = []

    # ✅ Trường hợp phản ứng tích cực mạnh
    if funding > 0.008 and volume > 30 and rsi > 55 and spread < 1.2:
        signals.append("✅ Thị trường phản ứng tích cực mạnh → có thể cân nhắc Long")

    # 🔴 Phản ứng tiêu cực đáng ngại
    elif funding < -0.008 and rsi < 45 and spread > 1.3:
        signals.append("🔴 Phản ứng tiêu cực → nên đứng ngoài để tránh nhiễu")

    # 💡 Biến động mạnh nhưng ổn định
    elif volume > 35 and spread < 1.1:
        signals.append("💡 Volume mạnh, spread ổn định → có thể canh breakout nếu giá xác nhận")

    # 🤔 Tâm lý tốt nhưng lực giao dịch yếu
    elif funding > 0.006 and volume < 20:
        signals.append("🤔 Tâm lý tốt nhưng lực giao dịch yếu → cần chờ thêm xác nhận")

    else:
        signals.append("⚠️ Dữ liệu chưa rõ ràng → nên theo dõi thêm trước khi vào lệnh")

    # 📣 Gợi ý thêm theo ngữ cảnh tin tức nếu có
    if news_context:
        if impact in ["high", "very high", "rất cao", "cao"]:
            signals.append("📣 Lưu ý: Đây là sự kiện vĩ mô có độ ảnh hưởng lớn — cần quản trị rủi ro tốt.")
        if event_type in ["cpi", "nonfarm", "fomc", "lãi suất"]:
            signals.append(f"🧾 Tin `{event_type.upper()}` thường gây biến động mạnh trong 5–15 phút đầu sau khi công bố.")

    return signals
