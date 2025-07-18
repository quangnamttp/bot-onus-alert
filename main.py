import os
from flask import Flask, request
import mess_handler  # module xử lý webhook

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot Cofure đang chạy ✅", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = os.getenv("VERIFY_TOKEN")
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            print("✅ Webhook xác thực thành công")
            return challenge, 200
        else:
            print("❌ Webhook xác thực thất bại")
            return "Forbidden", 403

    elif request.method == "POST":
        return mess_handler.webhook()

# Khởi động bot
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
