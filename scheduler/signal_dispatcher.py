# cofure_bot/scheduler/signal_dispatcher.py

import logging
from core.signal_generator import generate_signals
from messages.format_signal import format_signal_batch
from messenger.send_message import send_message
from utils.signal_switch import is_signal_enabled

def send_trade_signals(user_id):
    try:
        if not is_signal_enabled():
            logging.info("🔕 Radar tắt — không gửi bản tin phiên")
            return

        signals = generate_signals()
        logging.info(f"📊 Tín hiệu phiên tìm được: {len(signals)}")

        if not signals:
            send_message(user_id, "🔕 Hiện tại chưa có tín hiệu phiên đủ điều kiện.")
            logging.info("📤 Đã gửi thông báo không có tín hiệu")
        else:
            formatted = format_signal_batch(signals)
            logging.info(f"📩 Nội dung bản tin phiên:\n{formatted}")
            send_message(user_id, formatted)
            logging.info("📤 Đã gửi bản tin phiên thành công")

    except Exception:
        logging.exception("❌ Lỗi khi gửi tín hiệu phiên")
