# schedule_trigger.py

from core.multi_signal_manager import generate_batch_signals
from core.liquidity_alert_runner import check_liquidity_batch
from scheduler.morning_reporter import get_morning_report
from scheduler.economic_calendar import scrape_calendar
from scheduler.event_watcher import post_event_analysis
from scheduler.night_summary import wrap_up_day
from config import SCHEDULE_TIMES

def run_scheduled_tasks(current_time):
    output = []

    # 📌 Mốc 06:00 → bản tin sáng
    if current_time == SCHEDULE_TIMES["morning_brief"]:
        output.append(get_morning_report())

    # 📌 Mốc 07:00 → lịch kinh tế
    if current_time == SCHEDULE_TIMES["economic_calendar"]:
        output.append(scrape_calendar())

    # 📌 Mốc mỗi 15 phút → tín hiệu kỹ thuật
    if current_time.endswith(tuple(SCHEDULE_TIMES["signal_generator"])):
        coins = ["BTC", "ETH", "SOL", "XRP"]
        signals = generate_batch_signals(coins, "Binance")
        output.extend(signals)

    # 📌 Mốc 19:30 → phân tích sau tin
    if current_time == SCHEDULE_TIMES["event_watcher"]:
        output.append(post_event_analysis())

    # 📌 Mốc 22:00 → tổng kết phiên
    if current_time == SCHEDULE_TIMES["night_summary"]:
        output.append(wrap_up_day())

    # 📌 Quét dòng tiền liên tục
    liquidity_alerts = check_liquidity_batch(["BTC", "ETH", "SOL"])
    output.extend(liquidity_alerts)

    return output
