from flask import Flask, request
from messenger.mess_handler import handle_new_message
from utils.config_loader import VERIFY_TOKEN

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
            msg_text = msg_event.get("message", {}).get("text", "")
            user_name = "Trader"  # 👤 Tên mặc định, có thể mở rộng lấy tên thật sau này

            if msg_text:
                handle_new_message(user_id, user_name, msg_text)
                print(f"[main] → {user_id}: tin nhắn đã được xử lý.")
    return "OK", 200

# ✅ Khởi chạy server Flask
if __name__ == "__main__":
    app.run(debug=True, port=5000)
