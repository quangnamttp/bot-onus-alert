from datetime import datetime

def get_today_events():
    today = datetime.now().strftime("%d/%m/%Y")
    events = {
        "16/07/2025": [
            "🇯🇵 07:30 — GDP Nhật Bản",
            "🇺🇸 19:30 — CPI Hoa Kỳ",
            "🇺🇸 22:00 — Phát biểu Chủ tịch Fed"
        ],
        "17/07/2025": [
            "🇬🇧 13:00 — CPI Anh Quốc",
            "🇪🇺 14:00 — Lãi suất ECB"
        ]
    }

    today_events = events.get(today, [])
    if not today_events:
        return f"📆 Không có tin vĩ mô quan trọng nào trong ngày {today}"

    return (
        f"📆 Lịch kinh tế hôm nay ({today}) — nguồn: ForexFactory.com\n" +
        "\n".join(f"— {e}" for e in today_events) +
        "\n\n⚠️ Các tin này có thể gây biến động mạnh với thị trường crypto\n"
        "→ Tránh mở lệnh trước giờ tin ra | Ưu tiên Scalp sau tin nếu volume đẩy mạnh"
    )
