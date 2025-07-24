# cofure_bot/main.py

from flask import Flask, request
from messenger.send_message import (
    send_message,
    send_template_message,
    send_button_template
)
from scheduler.signal_dispatcher import send_trade_signals
from scheduler.morning_report import send_morning_report
from scheduler.news_schedule import send_macro_news
from scheduler.summary_report import send_summary_report
from scheduler.emergency_trigger import run_emergency_loop
from utils.config_loader import VERIFY_TOKEN, MY_USER_ID, PORT
from utils.signal_switch import toggle_signal, is_signal_enabled

import schedule, threading, time, logging
from datetime import datetime

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
    token    = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    return challenge if token == VERIFY_TOKEN else "Sai token", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    logging.info(f"📩 Nhận Messenger: {data}")
    event = data["entry"][0]["messaging"][0]

    if "message" in event and "text" in event["message"]:
        text      = event["message"]["text"].lower().strip()
        sender_id = event["sender"]["id"]

        if "bật tín hiệu" in text or text == "on":
            toggle_signal("on")
            send_message(sender_id, "✅ Cofure đã bật tín hiệu. Radar đang hoạt động.")
            send_trade_signals(sender_id)              # ← Gửi ngay tín hiệu
            send_macro_news(sender_id, date="today", use_template=True)  # ← Gửi lịch ngay

        elif "tắt tín hiệu" in text or text == "off":
            toggle_signal("off")
            send_message(sender_id, "🔕 Cofure đã tắt tín hiệu. Bot ngưng hoạt động tự động.")

        elif "trạng thái" in text:
            status = "bật 🟢" if is_signal_enabled() else "tắt 🔴"
            send_message(sender_id, f"📡 Radar Cofure đang ở chế độ {status}.")

        elif "lịch hôm nay" in text:
            send_macro_news(sender_id, date="today", use_template=True)

        elif "lịch ngày mai" in text:
            send_macro_news(sender_id, date="tomorrow", use_template=True)

        elif "lịch tuần" in text or "lịch cả tuần" in text:
            send_macro_news(sender_id, date_range="week", use_template=True)

        else:
            send_message(sender_id, f"📩 Cofure nhận được: “{text}”")

    return "OK", 200


def start_scheduler():
    logging.info("🟢 start_scheduler() has started")
    logging.info("🕒 Giờ hệ thống hiện tại: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 06:00 Morning report
    def job_morning():
        logging.info("🌞 [Scheduler] Kích báo cáo sáng")
        if is_signal_enabled():
            send_morning_report(MY_USER_ID)
    schedule.every().day.at("06:00").do(job_morning)

    # 07:00 Macro news
    def job_macro():
        logging.info("📅 [Scheduler] Kích lịch vĩ mô")
        if is_signal_enabled():
            send_macro_news(MY_USER_ID, use_template=True)
    schedule.every().day.at("07:00").do(job_macro)

    # 06:00–21:45: trade signals mỗi 15 phút
    def job_trade(ts):
        logging.info(f"📡 [Scheduler] Kích gửi tín hiệu tại {ts}")
        if is_signal_enabled():
            send_trade_signals(MY_USER_ID)
    for h in range(6, 22):
        for m in [0, 15, 30, 45]:
            ts = f"{h:02d}:{m:02d}"
            schedule.every().day.at(ts).do(lambda ts=ts: job_trade(ts))

    # 22:00 Summary report
    def job_summary():
        logging.info("🌙 [Scheduler] Kích tổng kết tối")
        if is_signal_enabled():
            send_summary_report(MY_USER_ID)
    schedule.every().day.at("22:00").do(job_summary)

    # Vòng lặp pending + heartbeat
    last_log = time.time()
    while True:
        schedule.run_pending()
        if time.time() - last_log > 30:
            logging.info("⏳ Vòng lặp scheduler đang hoạt động bình thường")
            last_log = time.time()
        time.sleep(1)


def start_emergency_radar():
    logging.info("🔴 Radar khẩn cấp đã bật")
    run_emergency_loop()


if __name__ == "__main__":
    logging.info("🚀 Cofure Bot khởi động")
    send_message(MY_USER_ID, "✅ Cofure đã khởi động thành công và đang chờ tín hiệu.")

    # Khởi radar khẩn cấp
    start_emergency_radar()

    # Khởi scheduler nền
    sched_thread = threading.Thread(target=start_scheduler, daemon=True)
    sched_thread.start()
    logging.info(f"🧵 Scheduler thread is_alive: {sched_thread.is_alive()}")

    # Chạy Flask
    app.run(host="0.0.0.0", port=PORT)
