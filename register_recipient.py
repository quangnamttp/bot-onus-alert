from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == "cofure_verify_2025":
        return request.args.get("hub.challenge")
    return "Invalid token", 403

@app.route("/webhook", methods=["POST"])
def receive():
    try:
        psid = request.get_json()["entry"][0]["messaging"][0]["sender"]["id"]
        update_list(psid)
        setup_exchange(psid)
    except Exception as e:
        print(f"⚠️ Cannot extract PSID: {e}")
    return "ok", 200

def update_list(psid):
    try:
        with open("recipient_list.json") as f:
            data = json.load(f)
    except:
        data = {"recipients": []}
    if psid not in data["recipients"]:
        data["recipients"].append(psid)
        with open("recipient_list.json", "w") as f:
            json.dump(data, f, indent=2)

def setup_exchange(psid):
    try:
        with open("user_config.json") as f:
            config = json.load(f)
    except:
        config = {}
    if psid not in config:
        config[psid] = {"exchange": "onus"}
        with open("user_config.json", "w") as f:
            json.dump(config, f, indent=2)
