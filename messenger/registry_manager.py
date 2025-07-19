import json

def mark_pending(sender_id):
    path = "data/pending_users.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if sender_id not in data:
        data.append(sender_id)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

def is_pending(sender_id):
    path = "data/pending_users.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return sender_id in data
    except:
        return False

def is_registered(sender_id):
    path = "data/user_registry.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return sender_id in data
    except:
        return False
