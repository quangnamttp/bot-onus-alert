import json
from messenger.message_sender import send_message

def approve_user(psid):
    with open("data/user_registry.json", "r") as f:
        users = json.load(f)

    if psid not in users:
        users.append(psid)
        with open("data/user_registry.json", "w") as f:
            json.dump(users, f)

    # Xóa khỏi pending
    with open("data/pending_users.json", "r") as f:
        pending = json.load(f)
    if psid in pending:
        pending.remove(psid)
        with open("data/pending_users.json", "w") as f:
            json.dump(pending, f)

    send_message(psid, "✅ Bot Cofure đã được kích hoạt cho bạn!")

def reject_user(psid):
    with open("data/pending_users.json", "r") as f:
        pending = json.load(f)

    if psid in pending:
        pending.remove(psid)
        with open("data/pending_users.json", "w") as f:
            json.dump(pending, f)

    send_message(psid, "⛔ Bot Cofure không được kích hoạt cho bạn.")
