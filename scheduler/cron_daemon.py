import time
from scheduler.macro_reporter import send_morning_brief
from scheduler.signals import send_batch_signals
from scheduler.end_day_report import send_summary
from scheduler.reset_state import reset_all_data
from scheduler.macro_advisor import check_macro_alerts

def run_cron_loop():
    while True:
        now = time.localtime()
        hhmm = f"{now.tm_hour:02d}:{now.tm_min:02d}"

        if hhmm == "06:00":
            send_morning_brief()

        elif hhmm in ["06:15", "06:45", "07:15", "07:45", "08:15", "08:45",
                      "09:15", "09:45", "10:15", "10:45", "11:15", "11:45",
                      "12:15", "12:45", "13:15", "13:45", "14:15", "14:45",
                      "15:15", "15:45", "16:15", "16:45", "17:15", "17:45",
                      "18:15", "18:45", "19:15", "19:45", "20:15", "20:45",
                      "21:15", "21:45"]:
            send_batch_signals()

        elif hhmm == "07:00":
            check_macro_alerts()

        elif hhmm == "22:00":
            send_summary()

        elif hhmm == "23:00":
            reset_all_data()

        time.sleep(55)
