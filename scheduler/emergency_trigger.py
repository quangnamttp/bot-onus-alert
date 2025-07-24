# cofure_bot/scheduler/emergency_trigger.py

import threading, time
from core.emergency_signal import run_emergency_monitor
from utils.signal_switch import is_signal_enabled  # ← Thêm import công tắc

def run_emergency_loop():
    def loop():
        while True:
            if is_signal_enabled():
                run_emergency_monitor()
            time.sleep(60)  # Chạy mỗi phút nếu công tắc đang ON
    threading.Thread(target=loop, daemon=True).start()
