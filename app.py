from flask import Flask, request
import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot ONUS Flask đang hoạt động!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Sai verify token", 403

    elif request.method == "POST":
        data = request.get_json()
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                if "message" in messaging_event:
                    send_message(sender_id)
        return "OK", 200

def send_message(user_id):
    token_data = fetch_onus_data()
    message = f"📊 Token đang pump:\n" + "\n".join(token_data)
    url = "https://graph.facebook.com/v17.0/me/messages"
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": message},
        "messaging_type": "RESPONSE",
        "access_token": PAGE_ACCESS_TOKEN
    }
    requests.post(url, json=payload)

def fetch_onus_data():
    resp = requests.get("https://goonus.io/")
    soup = BeautifulSoup(resp.text, "html.parser")
    tokens = []
    for card in soup.select(".market-card")[:3]:
        name = card.select_one(".name").text
        price = card.select_one(".price").text
        percent = card.select_one(".percent").text
        tokens.append(f"🔥 {name}: {price} ({percent})")
    return tokens

if __name__ == "__main__":
    app.run(debug=True)
