# night_summary.py

def nightly_summary(trade_stats):
    long_count = trade_stats.get("long", 0)
    short_count = trade_stats.get("short", 0)
    total = long_count + short_count
    long_ratio = round(long_count / total * 100, 1) if total else 0

    return (
        "🌙 Chúc ngủ ngon trader!\n\n"
        f"📊 Tổng kết hôm nay:\n"
        f"→ Lệnh Long: {long_count} | Short: {short_count}\n"
        f"→ Tỷ lệ Long: {long_ratio}%\n\n"
        "🧠 Gợi ý: Kiểm tra lệnh còn mở trước khi qua phiên\n"
        "🔔 Theo dõi bản tin sáng mai lúc 06h00!"
    )
