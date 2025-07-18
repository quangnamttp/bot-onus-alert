from flask import Flask, request
from dotenv import load_dotenv
import os

# 🔐 Load biến môi trường từ file .env
load_dotenv()

app = Flask(__name__)

# 🎯 Route webhook để nhận và xác thực từ Meta
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Xác thực Webhook từ Meta Developer
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        verify_token = os.getenv("VERIFY_TOKEN")

        if mode == "subscribe" and token == verify_token:
            print("✅ Webhook đã xác thực từ Meta")
            return challenge, 200
        else:
            print("❌ Webhook xác thực thất bại")
            return "Verification failed", 403

    elif request.method == 'POST':
        # Xử lý tin nhắn từ Messenger
        from messenger.mess_handler import handle_webhook
        return handle_webhook()

# ❌ KHÔNG gọi app.run() ở đây
# Vì Render sử dụng gunicorn: Procfile = "web: gunicorn main:app"
