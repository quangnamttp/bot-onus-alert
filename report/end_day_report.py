# end_day_report.py

def summarize_day(trade_log):
    total = len(trade_log)
    long_count = sum(1 for t in trade_log if t["type"] == "LONG")
    short_count = total - long_count
    win_count = sum(1 for t in trade_log if t["result"] == "TP")
    loss_count = sum(1 for t in trade_log if t["result"] == "SL")

    win_rate = round(win_count / total * 100, 1) if total else 0
    long_ratio = round(long_count / total * 100, 1) if total else 0

    return (
        "📊 Tổng kết phiên giao dịch hôm nay:\n\n"
        f"→ Số lệnh: {total}\n"
        f"→ Long: {long_count} | Short: {short_count} | Tỷ lệ Long: {long_ratio}%\n"
        f"→ TP: {win_count} | SL: {loss_count} | Winrate: {win_rate}%\n\n"
        "🧠 Gợi ý cho phiên mai: Kiểm tra lực đẩy từ khung H4 trở lên\n"
        "🔔 Đừng quên bản tin sáng lúc 06:00!"
    )
