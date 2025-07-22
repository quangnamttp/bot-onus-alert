from macro.news_analyzer import analyze_news_impact

def generate_macro_advice(news_title):
    impact = analyze_news_impact(news_title)
    if not impact:
        return f"🕯️ Tin {news_title} vừa ra, nhưng chưa có dữ liệu rõ ràng từ thị trường."

    if news_title == "US CPI":
        if impact["actual"] < impact["forecast"]:
            return f"🕯️ CPI ra: {impact['actual']}% (thấp hơn dự báo {impact['forecast']}%) → tâm lý tích cực.\n"
                   f"Funding BTC: {impact['funding_btc']}, Volume ETH: {impact['volume_eth']}.\n"
                   f"💡 Gợi ý: Có thể cân nhắc Long sau 5 phút nếu xu hướng ổn định."

        else:
            return f"🕯️ CPI ra: {impact['actual']}% (cao hơn dự báo) → thị trường biến động.\n"
                   f"💡 Gợi ý: Nên đứng ngoài 10–15 phút trước khi đánh giá lại."

    if news_title == "Biên bản họp FOMC":
        if "giữ nguyên" in impact["actual_rate"].lower():
            return f"🕯️ FED giữ lãi suất: {impact['actual_rate']} → thị trường đi ngang.\n"
                   f"💡 Gợi ý: Nên quan sát thêm, đứng ngoài ít phút sau tin."

        else:
            return f"🕯️ FED điều chỉnh lãi suất: {impact['actual_rate']} → thị trường có thể biến động mạnh.\n"
                   f"💡 Gợi ý: Cân nhắc lệnh chiến lược nếu phản ứng rõ xu hướng sau 5–10 phút."

    return "📊 Tin ra nhưng chưa rõ xu hướng. Nên chờ thị trường phản ứng trước khi hành động."
