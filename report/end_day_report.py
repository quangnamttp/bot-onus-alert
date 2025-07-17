def generate_report():
    # ⚠️ Dữ liệu giả lập (sau này có thể lấy từ logger hoặc file thực)
    trades = [
        {"symbol": "BTCUSDT", "type": "LONG", "rr": 1.5},
        {"symbol": "ETHUSDT", "type": "SHORT", "rr": 1.2},
        {"symbol": "MATICUSDT", "type": "LONG", "rr": 0.9},
        {"symbol": "OPUSDT", "type": "LONG", "rr": 1.3},
        {"symbol": "SOLUSDT", "type": "SHORT", "rr": 1.1}
    ]

    total = len(trades)
    rr_list = [t["rr"] for t in trades]
    avg_rr = round(sum(rr_list) / total, 2) if total > 0 else "N/A"

    long_count = sum(1 for t in trades if t["type"] == "LONG")
    short_count = sum(1 for t in trades if t["type"] == "SHORT")

    pct_long = round(long_count * 100 / total, 1) if total > 0 else 0
    pct_short = round(short_count * 100 / total, 1) if total > 0 else 0

    summary = (
        "📊 Tổng kết Cofure hôm nay:\n"
        f"🔁 R:R trung bình: {avg_rr}\n"
        f"📈 Tổng số lệnh: {total} (🔥 {long_count} MUA / 🧊 {short_count} BÁN)\n"
        f"📊 Tỷ lệ: {pct_long}% MUA — {pct_short}% BÁN\n"
        "🌙 Chúc cả team ngủ ngon!"
    )
    return summary
