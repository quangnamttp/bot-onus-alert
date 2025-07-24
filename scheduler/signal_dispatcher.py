import logging
from core.signal_generator import generate_signals
from messages.format_signal import format_signal_batch
from messenger.send_message import send_message
from utils.config_loader import MY_USER_ID
from utils.signal_switch import is_signal_enabled  # ⬅️ Bổ sung dòng này

def send_trade_signals(user_id):
    if not is_signal_enabled():  # ⬅️ Kiểm tra trạng thái radar
        logging.info("🔕 Radar đang tắt — không gửi bản tin phiên")
        return

    signals = generate_signals()
    logging.info(f"📊 Số lượng tín hiệu phiên tìm thấy: {len(signals)}")

    if not signals:
        send_message(user_id, "🔕 Hiện tại chưa có tín hiệu phiên nào đủ điều kiện.")
        logging.info("📤 Đã gửi thông báo không có tín hiệu")
        return

    formatted = format_signal_batch(signals)
    logging.info(f"📩 Nội dung bản tin phiên:\n{formatted}")
    send_message(user_id, formatted)
    logging.info("📤 Đã gửi bản tin phiên thành công")
