import time
from scheduler.macro_reporter import morning_macro_report

def run_cron():
    while True:
        now = time.strftime("%H:%M")
        if now == "06:00":
            morning_macro_report()
        time.sleep(60)
