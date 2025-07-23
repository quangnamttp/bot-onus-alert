import json
import os

DATA_FILE = "user_status.json"  # 📁 File lưu trạng thái từng user

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def register_user(user_id, user_name):
    data = load_data()
    data[user_id] = {
        "name": user_name,
        "approved": False,
        "signal_active": False
    }
    save_data(data)

def get_user_status(user_id):
    return load_data().get(user_id)

def update_user_status(user_id, key, value):
    data = load_data()
    if user_id in data:
        data[user_id][key] = value
        save_data(data)

def approve_user(user_id):
    update_user_status(user_id, "approved", True)
    update_user_status(user_id, "signal_active", True)
