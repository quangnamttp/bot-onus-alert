import json

def user_registry_path():
    return "data/user_registry.json"

def mark_registered(sender_id):
    path = user_registry_path()
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if sender_id not in data:
        data.append(sender_id)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

def is_registered(sender_id):
    path = user_registry_path()
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return sender_id in data
    except:
        return False

def get_all_registered_users():
    path = user_registry_path()
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []
