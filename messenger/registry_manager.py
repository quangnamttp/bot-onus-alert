import json
import os

REGISTRY_PATH = "data/user_registry.json"

def mark_registered(sender_id):
    if not os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "w") as f:
            json.dump([], f)

    try:
        with open(REGISTRY_PATH, "r") as f:
            users = json.load(f)
        if sender_id not in users:
            users.append(sender_id)
            with open(REGISTRY_PATH, "w") as f:
                json.dump(users, f, indent=2)
    except:
        pass

def is_registered(sender_id):
    try:
        with open(REGISTRY_PATH, "r") as f:
            users = json.load(f)
        return sender_id in users
    except:
        return False

def remove_from_registry(sender_id):
    try:
        with open(REGISTRY_PATH, "r") as f:
            users = json.load(f)
        users = [u for u in users if u != sender_id]
        with open(REGISTRY_PATH, "w") as f:
            json.dump(users, f, indent=2)
    except:
        pass

def get_all_registered_users():
    try:
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)
    except:
        return []
