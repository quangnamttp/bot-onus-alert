from flask import Flask, request
from messenger.mess_handler import handle_message
from init_files import init_bot_files
import os

app = Flask(__name__)
init_bot_files()

@app.route('/webhook', methods=['GET'])
def verify():
    verify_token = os.getenv("VERIFY_TOKEN", "")
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == verify_token:
        return request.args.get("hub.challenge"), 200
    return "Invalid token", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                if "message" in event and "text" in event["message"]:
                    handle_message(event)
    return "OK", 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
