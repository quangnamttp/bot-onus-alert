# cofure_bot/main.py

from flask import Flask, request
from messenger.send_message import send_message
from scheduler.signal_dispatcher import send_trade_signals
from scheduler.morning_report import send_morning_report
from scheduler.news_schedule import send_macro_news
from scheduler.summary_report import send_summary_report
from scheduler.emergency_trigger import run_emergency_loop
from utils.config_loader import VERIFY_TOKEN, MY_USER_ID, PORT
from utils.signal_switch import toggle_signal, is_signal_enabled

import schedule, threading, time, logging

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)


@app.route("/", methods=["GET", "POST"])
def home():
    return "✅ Cofure Bot đang hoạt động 🎯", 200


@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    return challenge if token == VERIFY_TOKEN else "Sai token", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    logging.info(f"📩 Nhận Messenger: {data}")
    messaging_event = data["entry"][0]["messaging"][0]

    if "message" in messaging_event and "text" in messaging_event["message"]:
        text = messaging_event["message"]["text"].lower().strip()
        sender_id = messaging_event["sender"]["id"]

        if "bật tín hiệu" in text or text == "on":
            toggle_signal("on")
            send_message(sender_id, "✅ Cofure đã bật tín hiệu. Radar đang hoạt động.")
        elif "tắt tín hiệu" in text or text == "off":
            toggle_signal("off")
            send_message(sender_id, "🔕 Cofure đã tắt tín hiệu. Bot ngưng hoạt động tự động.")
        elif "trạng thái" in text:
            status = "bật 🟢" if is_signal_enabled() else "tắt 🔴"
            send_message(sender_id, f"📡 Radar Cofure đang ở chế độ {status}.")
        elif "lịch hôm nay" in text:
            send_macro_news(sender_id, date="today")
        elif "lịch ngày mai" in text:
            send_macro_news(sender_id, date="tomorrow")
        elif "lịch tuần" in text or "lịch cả tuần" in text:
            send_macro_news(sender_id, date_range="week")
        else:
            send_message(sender_id, f"📩 Cofure nhận được: “{text}”")

    return "OK", 200


def start_scheduler():
    logging.info("🟢 start_scheduler() has started")

    # Báo cáo sáng 06:00
    def job_morning():
        if is_signal_enabled():
            logging.info("🌞 Running send_morning_report()")
            send_morning_report(MY_USER_ID)
    schedule.every().day.at("06:00").do(job_morning)
    logging.info("🔧 Scheduled morning report at 06:00")

    # Lịch vĩ mô 07:00
    def job_macro():
        if is_signal_enabled():
            logging.info("📰 Running send_macro_news()")
            send_macro_news(MY_USER_ID)
    schedule.every().day.at("07:00").do(job_macro)
    logging.info("🔧 Scheduled macro news at 07:00")

    # Tín hiệu giao dịch từ 06:00 → 21:45 mỗi 15 phút
    def job_trade(ts):
        if is_signal_enabled():
            logging.info(f"📡 Running send_trade_signals() at {ts}")
            send_trade_signals(MY_USER_ID)
    for hour in range(6, 22):
        for minute in [0, 15, 30, 45]:
            ts = f"{hour:02d}:{minute:02d}"
            schedule.every().day.at(ts).do(lambda ts=ts: job_trade(ts))
            logging.info(f"🔧 Scheduled trade signal at {ts}")

    # Tổng kết tối 22:00
    def job_summary():
        if is_signal_enabled():
            logging.info("🌙 Running send_summary_report()")
            send_summary_report(MY_USER_ID)
    schedule.every().day.at("22:00").do(job_summary)
    logging.info("🔧 Scheduled summary report at 22:00")

    # Vòng lặp pending
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_emergency_radar():
    logging.info("🔴 Radar khẩn cấp đã bật")
    # run_emergency_loop() vốn đã spawn thread bên trong, chỉ cần gọi một lần
    run_emergency_loop()


if __name__ == "__main__":
    logging.info("🚀 Cofure Bot khởi động")

    # Test gửi tin khởi động
    send_message(MY_USER_ID, "✅ Cofure đã khởi động thành công và đang chờ tín hiệu.")

    # Radar khẩn cấp
    start_emergency_radar()

    # Scheduler chạy nền
    sched_thread = threading.Thread(target=start_scheduler, daemon=True)
    sched_thread.start()
    logging.info(f"🧵 Scheduler thread is_alive: {sched_thread.is_alive()}")

    # Chạy Flask app
    app.run(host="0.0.0.0", port=PORT)
