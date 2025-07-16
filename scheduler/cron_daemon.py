# cron_daemon.py

import time
from datetime import datetime
from scheduler.schedule_trigger import run_scheduled_tasks

def loop_scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        results = run_scheduled_tasks(now)
        for item in results:
            print(item)
        time.sleep(60)
