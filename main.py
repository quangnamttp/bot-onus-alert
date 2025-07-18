from flask import Flask
from messenger.mess_handler import handle_webhook

app = Flask(__name__)

# 📡 Route nhận Webhook từ Facebook Messenger
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    return handle_webhook()

# ✅ Route kiểm tra bot đang chạy
@app.route("/")
def home():
    return "🔧 Cofure Bot đang hoạt động!"

# 🚀 Khởi động Flask server
if __name__ == "__main__":
    app.run(debug=True)
