from flask import Flask, request
from messenger.mess_handler import handle_new_message
from utils.config_loader import VERIFY_TOKEN

app = Flask(__name__)

@app.route("/", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    return challenge if token == VERIFY_TOKEN else "Invalid token"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    for entry in data.get("entry", []):
        for msg_event in entry.get("messaging", []):
            user_id = msg_event["sender"]["id"]
            msg_text = msg_event.get("message", {}).get("text", "")
            user_name = "Trader"  # Tùy chỉnh nếu lấy được tên thật
            response = handle_new_message(user_id, user_name, msg_text)
            print(f"[main] → {user_id}: {response['text']}")
    return "OK", 200

if __name__ == "__main__":
    app.run()
