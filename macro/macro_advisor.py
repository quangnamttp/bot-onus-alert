# cofure_bot/macro/macro_advisor.py

def generate_macro_strategy(news_list):
    if not news_list:
        return "📅 Hôm nay không có tin tức vĩ mô quan trọng.\nChúc bạn một ngày trade thật tự tin nhé!"

    lines = ["📅 Tin vĩ mô hôm nay bạn cần chú ý:\n"]
    for item in news_list:
        impact = "🔥" if item["impact"] == "High" else "⚠️"
        lines.append(f"{impact} {item['time']} — {item['title']} ({item['impact']})")

    lines.append("\n📋 Gợi ý: Nếu tin ra lúc 20:30 thì nên đứng ngoài 5 phút sau đó hãy vào lệnh nếu thị trường ổn định.")
    return "\n".join(lines)
