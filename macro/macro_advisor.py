def generate_macro_strategy(news_list, date_label="hôm nay"):
    if not news_list:
        return f"📅 Không có tin tức vĩ mô quan trọng {date_label}.\nChúc bạn một ngày trade thật tự tin nhé!"

    lines = [f"📅 Tin vĩ mô {date_label} bạn cần chú ý:\n"]
    for item in news_list:
        impact = "🔥" if item.get("impact") == "High" else "⚠️"
        time = item.get("time", "⏰?")
        title = item.get("title", "Không rõ nội dung")
        lines.append(f"{impact} {time} — {title} ({item['impact']})")

    lines.append("\n📋 Gợi ý: Nếu tin ra lúc 20:30 thì nên đứng ngoài 5 phút sau đó hãy vào lệnh nếu thị trường ổn định.")
    return "\n".join(lines)
