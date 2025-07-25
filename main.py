from flask import Flask, request
from messenger.send_message import send_message
from scheduler.signal_dispatcher import send_trade_signals
from scheduler.morning_report import send_morning_report
from scheduler.news_schedule import send_macro_news
from scheduler.summary_report import send_summary_report
from scheduler.emergency_trigger import run_emergency_loop
from utils.config_loader import VERIFY_TOKEN, MY_USER_ID, PORT, TZ
from utils.signal_switch import toggle_signal, is_signal_enabled

import schedule, threading, time, logging, requests
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

@app.route("/", methods=["GET"])
def home():
    return "✅ Cofure Bot đang hoạt động 🎯", 200

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    logging.info(f"🔍 Xác minh webhook: token={token}")
    if token == VERIFY_TOKEN and challenge:
        logging.info("✅ Xác minh thành công")
        return str(challenge)
    else:
        logging.warning("❌ Token không hợp lệ")
        return "Sai token", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    try:
        data = request.get_json(force=True)
        logging.info(f"📩 POST từ Messenger: {data}")
        event = data.get("entry", [{}])[0].get("messaging", [{}])[0]
        sender_id = event.get("sender", {}).get("id")
        message = event.get("message", {}).get("text", "").lower().strip()

        if not sender_id:
            logging.warning("⚠️ Thiếu sender_id")
            return "OK", 200

        if message:
            if "bật tín hiệu" in message or message == "on":
                toggle_signal("on")
                send_message(sender_id, "✅ Radar Cofure đã bật.")
                send_trade_signals(sender_id)
                send_macro_news(sender_id, date="today", use_template=True)

            elif "tắt tín hiệu" in message or message == "off":
                toggle_signal("off")
                send_message(sender_id, "🔕 Cofure đã tắt tín hiệu.")

            elif "trạng thái" in message:
                status = "bật 🟢" if is_signal_enabled() else "tắt 🔴"
                send_message(sender_id, f"📡 Radar đang ở chế độ {status}.")

            elif "lịch hôm nay" in message:
                if not send_macro_news(sender_id, date="today", use_template=True):
                    send_message(sender_id, "📭 Hôm nay không có lịch hoặc lỗi khi kết nối dữ liệu.")

            elif "lịch ngày mai" in message:
                if not send_macro_news(sender_id, date="tomorrow", use_template=True):
                    send_message(sender_id, "📭 Ngày mai không có lịch hoặc lỗi dữ liệu.")

            elif "lịch tuần" in message:
                if not send_macro_news(sender_id, date_range="week", use_template=True):
                    send_message(sender_id, "📭 Tuần này không có lịch hoặc lỗi dữ liệu.")

            else:
                send_message(sender_id, f"📨 Cofure nhận: “{message}”")

        return "OK", 200

    except Exception as e:
        logging.exception(f"❌ Lỗi xử lý Messenger: {e}")
        return "OK", 200

@app.route("/ping", methods=["GET"])
def ping():
    logging.info("📶 Ping giữ bot tỉnh")
    return "pong", 200

def keep_alive_ping():
    def loop():
        while True:
            try:
                requests.get(f"http://localhost:{PORT}/ping")
                logging.info("📶 Tự ping thành công")
            except:
                logging.warning("❌ Ping thất bại")
            time.sleep(300)
    threading.Thread(target=loop, daemon=True).start()

def start_scheduler():
    logging.info("🟢 Bắt đầu scheduler")
    logging.info("🕒 Giờ VN: %s", datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S"))

    def job_morning():
        if is_signal_enabled():
            send_morning_report(MY_USER_ID)
    schedule.every().day.at("06:00").do(job_morning)

    def job_macro():
        if is_signal_enabled():
            send_macro_news(MY_USER_ID, use_template=True)
    schedule.every().day.at("07:00").do(job_macro)

    def job_trade(ts):
        if is_signal_enabled():
            send_trade_signals(MY_USER_ID)
    for h in range(6, 22):
        for m in [0, 15, 30, 45]:
            ts = f"{h:02d}:{m:02d}"
            schedule.every().day.at(ts).do(lambda ts=ts: job_trade(ts))

    def job_summary():
        if is_signal_enabled():
            send_summary_report(MY_USER_ID)
    schedule.every().day.at("22:00").do(job_summary)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_emergency_radar():
    logging.info("🔴 Radar khẩn cấp bật")
    run_emergency_loop()

if __name__ == "__main__":
    logging.info("🚀 Khởi động Cofure Bot")
    send_message(MY_USER_ID, "✅ Cofure đã khởi động và sẵn sàng nhận tín hiệu.")
    start_emergency_radar()
    keep_alive_ping()
    threading.Thread(target=start_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
