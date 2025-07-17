from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.signal_generator import run_signal_batch
from scheduler.morning_reporter import send_morning_news
from scheduler.auto_reporter import send_summary
from scheduler.event_watcher import check_macro_event
from scheduler.night_summary import reset_data

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(send_morning_news, "cron", hour=6, minute=0)
    scheduler.add_job(run_signal_batch, "interval", minutes=20)
    scheduler.add_job(send_summary, "cron", hour=22, minute=0)
    scheduler.add_job(check_macro_event, "cron", hour=7, minute=0)
    scheduler.add_job(reset_data, "cron", hour=23, minute=0)

    scheduler.start()
    print("⏱ Scheduler running — tín hiệu Cofure tự động kích hoạt")
