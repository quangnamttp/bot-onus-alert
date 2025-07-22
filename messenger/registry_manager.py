import json
from datetime import datetime
from utils.logger import log

USER_FILE = "data/user_status.json"

def load_user_status():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_status(data):
    try:
        with open(USER_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        log(f"[registry_manager] Error saving user data: {e}")

def register_user(user_id, name):
    data = load_user_status()
    if user_id not in data:
        data[user_id] = {
            "name": name,
            "approved": False,
            "signal_active": False,
            "joined": datetime.now().isoformat()
        }
        save_user_status(data)
        log(f"[registry_manager] New user registered: {user_id}")

def update_user_status(user_id, key, value):
    data = load_user_status()
    if user_id in data:
        data[user_id][key] = value
        save_user_status(data)
        log(f"[registry_manager] Updated {key} for {user_id} → {value}")

def get_user_status(user_id):
    data = load_user_status()
    return data.get(user_id, None)

def is_approved_and_active(user_id):
    user = get_user_status(user_id)
    return user and user.get("approved") and user.get("signal_active")
