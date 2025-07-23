# cofure_bot/scheduler/summary_report.py

from messenger.send_message import send_message

def send_summary_report(user_id):
    message = "🌒 Tổng kết phiên Cofure:\n• Hiệu suất: TP/SL 4/5 lệnh đạt target\n• Tỷ lệ: 62% Long • 38% Short\n\n📬 Dự báo ngày mai sẽ có sóng CHI và KAI breakout\n\n😴 Cảm ơn bạn đã đồng hành hôm nay — ngủ ngon nha  Anh Trương!"
    send_message(user_id, message)
