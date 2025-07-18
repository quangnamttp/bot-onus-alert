import json

def save_pending_user(psid):
    try:
        with open("data/pending_users.json", "r") as f:
            pending = json.load(f)
    except:
        pending = []

    if psid not in pending:
        pending.append(psid)
        with open("data/pending_users.json", "w") as f:
            json.dump(pending, f)
