# cofure_bot/main.py

from flask import Flask, request
from messenger.send_message import send_message
from scheduler.signal_dispatcher import send_trade_signals
from scheduler.morning_report import send_morning_report
from scheduler.news_schedule import send_macro_news
from scheduler.summary_report import send_summary_report
from scheduler.emergency_trigger import run_emergency_loop
from utils.config_loader import VERIFY_TOKEN, MY_USER_ID
import schedule, threading, time

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Cofure Bot đang hoạt động 🎯"

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    return challenge if token == VERIFY_TOKEN else "Sai token"

@app.route("/webhook", methods=["POST"])
def receive_message():
    return "OK", 200

def start_scheduler():
    # 🟢 Bản tin sáng + lịch vĩ mô
    schedule.every().day.at("06:00").do(lambda: send_morning_report(MY_USER_ID))
    schedule.every().day.at("07:00").do(lambda: send_macro_news(MY_USER_ID))

    # 📊 Gửi tín hiệu phiên mỗi 15 phút từ 06h → 22h
    for hour in range(6, 22):
        for minute in [0, 15, 30, 45]:
            timestamp = f"{hour:02d}:{minute:02d}"
            schedule.every().day.at(timestamp).do(lambda: send_trade_signals(MY_USER_ID))

    # 🌒 Tổng kết phiên lúc 22:00
    schedule.every().day.at("22:00").do(lambda: send_summary_report(MY_USER_ID))

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_emergency_radar():
    threading.Thread(target=run_emergency_loop, daemon=True).start()

if __name__ == "__main__":
    start_emergency_radar()    # 🔴 Radar khẩn cấp chạy liên tục
    threading.Thread(target=start_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
