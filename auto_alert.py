# auto_alert.py
import time
from signal_engine import scan_entry
from messenger import send_signal_to_all
from utils import format_signal
from subscribers import get_subscribers

def auto_loop():
    """Chạy vòng lặp gửi tín hiệu mỗi 15 phút"""
    while True:
        print("⏱️ Đang quét tín hiệu mới...")
        signals = scan_entry()
        if signals:
            users = get_subscribers()
            for sig in signals:
                message = format_signal(sig)
                for user_id in users:
                    send_signal_to_all(user_id, message)
        else:
            print("🚫 Không có tín hiệu phù hợp trong lần quét này.")
        time.sleep(900)  # 15 phút = 900 giây
