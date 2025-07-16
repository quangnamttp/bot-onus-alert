# main.py

import os
from dotenv import load_dotenv
from scheduler.schedule_trigger import run_scheduled_tasks
from datetime import datetime
import time

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
BOT_TOKEN = os.getenv("BOT_TOKEN")

def start_bot():
    print("🚀 Cofure Bot v1.5 khởi động...")
    print(f"🌐 Môi trường: {ENVIRONMENT}")
    print(f"🔐 Bot Token: {BOT_TOKEN[:5]}***")

    while True:
        now = datetime.now().strftime("%H:%M")
        results = run_scheduled_tasks(now)
        for r in results:
            print(r)
        time.sleep(60)

if __name__ == "__main__":
    start_bot()
