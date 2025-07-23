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
            user_name = "Trader"  # Có thể mở rộng lấy tên thật nếu cần

            if msg_text:
                response = handle_new_message(user_id, user_name, msg_text)
                print(f"[main] → {user_id}: {response['text']}")  # ✅ Chỉ log, không gửi lại
    return "OK", 200

# ✅ Khởi chạy server Flask
if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
