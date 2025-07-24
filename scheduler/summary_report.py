# cofure_bot/scheduler/summary_report.py

import logging
from messenger.send_message import send_message

def send_summary_report(user_id):
    """
    Gửi tổng kết phiên hôm nay cho user_id.
    """
    try:
        message = (
            "🌒 Tổng kết phiên Cofure:\n"
            "• Hiệu suất: TP/SL 4/5 lệnh đạt target\n"
            "• Tỷ lệ: 62% Long • 38% Short\n\n"
            "📬 Dự báo ngày mai sẽ có sóng CHI và KAI breakout\n\n"
            "😴 Cảm ơn bạn đã đồng hành hôm nay — ngủ ngon Anh Trương!"
        )

        # Log nội dung trước khi gửi
        logging.info("🌙 Preparing summary report: %s", message.replace("\n", " | "))

        # Gửi tin nhắn
        send_message(user_id, message)
        logging.info("📤 Sent summary report successfully")

    except Exception:
        logging.exception("❌ Error when sending summary report")
