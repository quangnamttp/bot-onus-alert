def nightly_summary(trade_stats):
    long = trade_stats.get("long", 0)
    short = trade_stats.get("short", 0)
    total = long + short
    long_ratio = round(long / total * 100, 1) if total else 0

    return (
        "🌙 Chúc ngủ ngon!\n"
        f"📊 Lệnh hôm nay: Long: {long} | Short: {short}\n"
        f"→ Tỷ lệ Long: {long_ratio}%\n"
        "🔔 Theo dõi bản tin sáng mai lúc 06:00 để chuẩn bị phiên mới!"
    )
