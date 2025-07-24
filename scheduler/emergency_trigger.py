# cofure_bot/scheduler/emergency_trigger.py

import threading
import time
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from core.emergency_signal import run_emergency_monitor
from utils.signal_switch import is_signal_enabled
from utils.config_loader import TZ

def run_emergency_loop():
    """
    Radar khẩn cấp chạy riêng thread mỗi phút.
    """
    def loop():
        logging.info("🔴 [Emergency] Thread radar khẩn cấp đã khởi chạy")
        while True:
            if is_signal_enabled():
                ts = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"📡 [Emergency] Kích monitor lúc {ts}")
                try:
                    run_emergency_monitor()
                    logging.info("✅ [Emergency] Monitor khẩn cấp hoàn tất")
                except Exception:
                    logging.exception("❌ [Emergency] Lỗi trong run_emergency_monitor()")
            else:
                logging.info("🔕 [Emergency] Công tắc tắt — không kiểm tra khẩn cấp")
            time.sleep(60)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
