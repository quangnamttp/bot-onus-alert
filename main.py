import os
import schedule
import time
from threading import Thread
from flask import Flask, request
from messenger.mess_handler import handle_new_message
from utils.config_loader import VERIFY_TOKEN

# ✅ Import các module gửi tín hiệu theo lịch
from scheduler.morning_report import send_morning_report
from scheduler.news_schedule import send_macro_news
from scheduler.signal_dispatcher import loop_send_trade_signals
from scheduler.summary_report import send_night_summary

app = Flask(__name__)

# ✅ Xác minh webhook từ Meta Developer
@app.route("/", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge, 200
    return "Invalid verification token", 403

# ✅ Xử lý tin nhắn POST từ Messenger
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    for entry in data.get("entry", []):
        for msg_event in entry.get("messaging", []):
            user_id = msg_event["sender"]["id"]
            user_name = "Trader"

            message = msg_event.get("message", {})
            if not message:
                continue

            # 📌 Nếu có phản hồi từ Quick Reply → truyền dict nguyên vẹn
            if "quick_reply" in message:
                handle_new_message(user_id, user_name, message)
            else:
                msg_text = message.get("text", "")
                if msg_text:
                    handle_new_message(user_id, user_name, msg_text)

            print(f"[main] → {user_id}: tin nhắn đã được xử lý.")
    return "OK", 200

# ✅ Khởi chạy lịch gửi tự động phần 2
def start_scheduler():
    schedule.every().day.at("06:00").do(send_morning_report)
    schedule.every().day.at("07:00").do(send_macro_news)
    schedule.every(15).minutes.do(loop_send_trade_signals)
    schedule.every().day.at("22:00").do(send_night_summary)

    while True:
        schedule.run_pending()
        time.sleep(10)

# ✅ Chạy Flask + scheduler song song
if __name__ == "__main__":
    Thread(target=start_scheduler).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
