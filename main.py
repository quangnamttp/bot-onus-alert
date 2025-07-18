from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()  # 🔐 Load biến môi trường từ file .env

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = os.getenv("VERIFY_TOKEN")
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            print("✅ Webhook đã xác thực với Meta")
            return challenge, 200
        else:
            return "❌ Xác thực thất bại", 403

    if request.method == 'POST':
        from messenger.mess_handler import handle_webhook
        return handle_webhook()

# ❌ KHÔNG GỒI app.run() ở cuối
# Vì bot sẽ được khởi động qua gunicorn: Procfile = "web: gunicorn main:app"
