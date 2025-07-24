# cofure_bot/scheduler/signal_dispatcher.py

import logging
from core.signal_generator import generate_signals
from messages.format_signal import format_signal_batch
from messenger.send_message import send_message
from utils.signal_switch import is_signal_enabled
from datetime import datetime
from pytz import timezone

VN_TZ = timezone("Asia/Ho_Chi_Minh")

def send_trade_signals(user_id):
    """
    Gửi bản tin tín hiệu phiên. Gọi mỗi 15 phút từ scheduler.
    Nếu không có tín hiệu đủ điều kiện thì gửi thông báo tương ứng.
    """
    try:
        if not is_signal_enabled():
            logging.info("🔕 Radar đã tắt — không gửi tín hiệu phiên")
            return

        now_str = datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"📡 Radar Cofure kích gửi tín hiệu lúc {now_str}")

        # 1. Gọi hàm tạo tín hiệu
        signals = generate_signals()
        logging.info(f"📊 Số lượng tín hiệu phiên tìm được: {len(signals)}")

        # 2. Nếu không có tín hiệu
        if not signals:
            msg = "🔕 Hiện tại chưa có tín hiệu phiên đủ điều kiện."
            send_message(user_id, msg)
            logging.info("📤 Đã gửi thông báo không có tín hiệu")
            return

        # 3. Format và gửi bản tin
        formatted = format_signal_batch(signals)
        logging.info(f"📩 Nội dung bản tin phiên:\n{formatted}")
        send_message(user_id, formatted)
        logging.info("📤 Đã gửi bản tin phiên thành công")

    except Exception:
        logging.exception("❌ Lỗi khi gửi bản tin tín hiệu phiên")
