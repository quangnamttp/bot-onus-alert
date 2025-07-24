from flask import Flask, request
from messenger.send_message import send_message
from scheduler.signal_dispatcher import send_trade_signals
from scheduler.morning_report import send_morning_report
from scheduler.news_schedule import send_macro_news
from scheduler.summary_report import send_summary_report
from scheduler.emergency_trigger import run_emergency_loop
from utils.config_loader import VERIFY_TOKEN, MY_USER_ID
from utils.signal_switch import toggle_signal, is_signal_enabled  # ⬅️ mới thêm
import schedule, threading, time, logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        logging.info("📩 Facebook gửi POST đến / — chưa xử lý")
        return "POST / không có xử lý", 200
    return "✅ Cofure Bot đang hoạt động 🎯", 200

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        logging.info("🔒 Xác thực webhook thành công")
        return challenge
    else:
        logging.warning("⛔ Sai VERIFY_TOKEN")
        return "Sai token", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    logging.info(f"📩 Nhận dữ liệu Messenger: {data}")
    messaging_event = data["entry"][0]["messaging"][0]

    if "message" in messaging_event and "text" in messaging_event["message"]:
        text = messaging_event["message"]["text"].lower()
        sender_id = messaging_event["sender"]["id"]

        if text == "on":
            toggle_signal("on")
            send_message(sender_id, "✅ Bot đã **bật tín hiệu**. Radar Cofure đang hoạt động.")
        elif text == "off":
            toggle_signal("off")
            send_message(sender_id, "🔕 Bot đã **tắt tín hiệu**. Radar Cofure sẽ ngưng phát sóng.")
        elif text == "trạng thái":
            status = "bật" if is_signal_enabled() else "tắt"
            send_message(sender_id, f"📡 Radar Cofure hiện đang **{status}**.")
        else:
            send_message(sender_id, f"📩 Cofure nhận được: “{text}”")

    return "OK", 200

def start_scheduler():
    logging.info("🟢 Scheduler bắt đầu chạy")

    schedule.every().day.at("06:00").do(lambda: send_morning_report(MY_USER_ID))
    schedule.every().day.at("07:00").do(lambda: send_macro_news(MY_USER_ID))

    for hour in range(6, 22):
        for minute in [0, 15, 30, 45]:
            timestamp = f"{hour:02d}:{minute:02d}"
            schedule.every().day.at(timestamp).do(
                lambda ts=timestamp: (
                    logging.info(f"📊 Gửi tín hiệu phiên lúc {ts}"),
                    send_trade_signals(MY_USER_ID)
                )
            )

    schedule.every().day.at("22:00").do(lambda: send_summary_report(MY_USER_ID))

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_emergency_radar():
    logging.info("🔴 Radar khẩn cấp đã bật")
    threading.Thread(target=run_emergency_loop, daemon=True).start()

if __name__ == "__main__":
    logging.info("🚀 Cofure Bot khởi động")
    send_message(MY_USER_ID, "✅ Cofure đã khởi động lại thành công và đang chạy tín hiệu!")
    start_emergency_radar()
    threading.Thread(target=start_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
