def format_morning_greeting(name, coin_data):
    msg = f"Chào buổi sáng nhé {name} ☀️\n\n📈 Dữ liệu thị trường:\n"
    for coin, data in coin_data.items():
        msg += f"• {coin}: Funding {data['funding']} • Giá: {data['price']:,} VNĐ\n"
    msg += "\n🌤️ Dự báo: Thị trường đang trong giai đoạn tích lũy, nên quan sát kỹ trước khi vào lệnh."
    return msg

def format_summary_report(name, performance):
    msg = f"🌒 Tổng kết phiên giao dịch hôm nay, {name}:\n\n"
    msg += f"• TP: {performance['tp']} lệnh\n"
    msg += f"• SL: {performance['sl']} lệnh\n"
    msg += f"• Tỷ lệ MUA: {performance['buy_rate']}%\n• Tỷ lệ BÁN: {performance['sell_rate']}%\n"
    msg += f"\n🔮 Dự báo ngày mai: {performance['next_trend']}\n"
    msg += "🌙 Cảm ơn bạn đã đồng hành cùng Cofure hôm nay. 😴 Ngủ ngon nha!"
    return msg
