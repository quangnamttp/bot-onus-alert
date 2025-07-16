# templates.py

def signal_template(coin, exchange, direction, entry, target, stoploss, strategy, analysis, rr):
    return (
        f"✅ #{coin.upper()} — {direction}\n"
        f"📍 Sàn: {exchange} | Khung: M15\n\n"
        f"{analysis}\n\n"
        f"🎯 Entry: ${entry} | Target: ${target} | SL: ${stoploss}\n"
        f"📌 Chiến lược: {strategy}\n{rr}"
    )

def calendar_template(events, date):
    return (
        f"📆 Lịch kinh tế hôm nay ({date}) — nguồn: ForexFactory.com\n" +
        "\n".join(f"— {e}" for e in events) +
        "\n\n⚠️ Các tin này có thể gây biến động mạnh với thị trường crypto\n"
        "→ Tránh mở lệnh trước giờ tin ra | Ưu tiên Scalp sau tin nếu volume đẩy mạnh"
    )
