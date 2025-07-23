# cofure_bot/scheduler/emergency_trigger.py

import threading, time
from core.emergency_signal import run_emergency_monitor

def run_emergency_loop():
    def loop():
        while True:
            run_emergency_monitor()
            time.sleep(60)  # Quét mỗi phút

    threading.Thread(target=loop, daemon=True).start()
