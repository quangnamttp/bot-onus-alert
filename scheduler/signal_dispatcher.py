# cofure_bot/scheduler/signal_dispatcher.py

import logging
from datetime import datetime
from utils.config_loader import TZ
from core.signal_generator import generate_signals
from messages.format_signal import format_signal_batch
from messenger.send_message import send_message
from utils.signal_switch import is_signal_enabled

def send_trade_signals(user_id):
    try:
        if not is_signal_enabled():
            logging.info("🔕 Radar đã tắt — không gửi tín hiệu phiên")
            return

        now_str = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"📡 [Scheduler] Gửi tín hiệu phiên lúc {now_str}")

        signals = generate_signals()
        logging.info(f"📊 Số tín hiệu tìm được: {len(signals)}")

        if not signals:
            send_message(user_id, "🔕 Hiện tại chưa có tín hiệu phiên đủ điều kiện.")
            logging.info("📤 Đã gửi: không có tín hiệu")
            return

        formatted = format_signal_batch(signals)
        logging.info(f"📩 Nội dung bản tin:\n{formatted}")
        send_message(user_id, formatted)
        logging.info("📤 Đã gửi bản tin tín hiệu thành công")

    except Exception:
        logging.exception("❌ Lỗi khi gửi bản tin tín hiệu phiên")
