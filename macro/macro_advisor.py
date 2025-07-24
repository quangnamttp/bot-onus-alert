# macro/macro_advisor.py

def generate_macro_strategy(news_list, date_label="hôm nay"):
    """
    Tạo chiến lược vĩ mô theo danh sách tin đã lọc (impact trung bình trở lên)
    """
    if not news_list:
        return f"📅 Không có tin tức vĩ mô quan trọng {date_label}.\nChúc bạn một ngày trade thật tự tin nhé!"

    news_list = sorted(news_list, key=lambda x: x.get("time", ""))

    lines = [f"📅 Tin vĩ mô {date_label} bạn cần chú ý:\n"]
    for item in news_list:
        impact  = item.get("impact", "Unknown").strip().lower()
        title   = item.get("title", "Không rõ nội dung")
        time    = item.get("time", "⏰?")
        country = item.get("country", "🌐")

        emoji = {
            "rất cao": "🔥", "very high": "🔥",
            "cao": "⚠️", "high": "⚠️",
            "trung bình": "🟡", "medium": "🟡"
        }.get(impact, "⚪")

        lines.append(f"{emoji} {time} — {country} {title} ({impact})")

    lines.append(
        "\n📋 Gợi ý: Với tin 🔥 hoặc ⚠️ sau 20:00, thị trường thường nhiễu mạnh. "
        "Hãy đứng ngoài vài phút sau khi tin ra để chờ ổn định rồi mới vào lệnh."
    )
    return "\n".join(lines)
