# mess_handler.py

from flask import Flask, request
import os
import requests
from userflow.coin_listener import CoinListener
from userflow.exchange_listener import ExchangeListener

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

coin_listener = CoinListener()
exchange_listener = ExchangeListener()

@app.route("/", methods=["GET"])
def verify_webhook():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token", 403

@app.route("/", methods=["POST"])
def receive_message():
    data = request.get_json()
    for entry in data.get("entry", []):
        for msg_event in entry.get("messaging", []):
            sender_id = msg_event["sender"]["id"]
            if "message" in msg_event and "text" in msg_event["message"]:
                user_text = msg_event["message"]["text"]
                reply = handle_message(user_text)
                send_message(sender_id, reply)
    return "ok", 200

def handle_message(text):
    text = text.strip().lower()

    # Nhận sàn
    exchange_reply = exchange_listener.update_exchange(text)
    if "✅" in exchange_reply:
        return exchange_reply

    # Nhận coin
    coin_reply = coin_listener.update_coin(text)
    if "✅" in coin_reply:
        return coin_reply

    # Phản hồi mặc định
    return f"🤖 Bot Cofure đã nhận: {text}\nGõ tên coin hoặc sàn để bắt đầu nhé!"

def send_message(recipient_id, message):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"[Messenger] Send message error: {e}")

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
