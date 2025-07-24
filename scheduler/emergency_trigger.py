# cofure_bot/scheduler/emergency_trigger.py

import threading, time, logging
from core.emergency_signal import run_emergency_monitor
from utils.signal_switch import is_signal_enabled
from datetime import datetime
from pytz import timezone

VN_TZ = timezone("Asia/Ho_Chi_Minh")

def run_emergency_loop():
    """
    Vòng lặp radar khẩn cấp — kiểm tra mỗi phút nếu công tắc đang bật.
    Dùng thread riêng không chặn scheduler chính.
    """
    def loop():
        logging.info("🔴 [Emergency] Đã khởi tạo vòng lặp radar khẩn cấp")
        while True:
            if is_signal_enabled():
                ts = datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"📡 [Emergency] Radar đang kích hoạt lúc {ts}")
                try:
                    run_emergency_monitor()
                    logging.info("✅ [Emergency] Kiểm tra khẩn cấp đã thực hiện xong")
                except Exception:
                    logging.exception("❌ [Emergency] Lỗi trong run_emergency_monitor()")
            else:
                logging.info("🔕 [Emergency] Công tắc đang tắt — radar khẩn cấp nghỉ")

            time.sleep(60)  # Kiểm tra mỗi 60s

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
    logging.info("🧵 [Emergency] Thread radar khẩn cấp đã khởi chạy")
