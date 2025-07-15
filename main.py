from emotion_handler.time_trigger import trigger_events
from scheduler.cron_manager import start_cron

if __name__ == "__main__":
    print("🚀 Cofure Bot v1.2 starting...")
    trigger_events()
    start_cron()


