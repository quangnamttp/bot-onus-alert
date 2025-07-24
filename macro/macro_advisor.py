def generate_macro_strategy(news_list, date_label="hôm nay"):
    if not news_list:
        return f"📅 Không có tin tức vĩ mô quan trọng {date_label}.\nChúc bạn một ngày trade thật tự tin nhé!"

    # 👉 Sắp xếp theo thời gian (tùy chọn, nếu API trả về đã có giờ chuẩn)
    news_list = sorted(news_list, key=lambda x: x.get("time", ""))

    lines = [f"📅 Tin vĩ mô {date_label} bạn cần chú ý:\n"]
    for item in news_list:
        impact_icon = "🔥" if item.get("impact") == "High" else "⚠️"
        time = item.get("time", "⏰?")
        title = item.get("title", "Không rõ nội dung")
        impact = item.get("impact", "Unknown")
        lines.append(f"{impact_icon} {time} — {title} ({impact})")

    lines.append("\n📋 Gợi ý: Nếu tin ra lúc 20:30 thì nên đứng ngoài 5 phút sau đó hãy vào lệnh nếu thị trường ổn định.")
    return "\n".join(lines)
