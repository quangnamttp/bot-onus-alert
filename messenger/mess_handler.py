from flask import request
from admin.config_loader import get_admin_psid
from admin.approval_handler import approve_user, reject_user
from messenger.message_sender import send_message
from messenger.registry_manager import save_pending_user

def handle_webhook():
    data = request.get_json()
    messaging_event = data["entry"][0]["messaging"][0]
    sender_id = messaging_event["sender"]["id"]
    message_text = messaging_event["message"].get("text", "")

    if sender_id == get_admin_psid():
        if message_text.startswith("/duyet "):
            psid = message_text.split("/duyet ")[1].strip()
            approve_user(psid)
        elif message_text.startswith("/huy "):
            psid = message_text.split("/huy ")[1].strip()
            reject_user(psid)
    else:
        save_pending_user(sender_id)
        send_message(sender_id, "🤖 Bot Cofure đã nhận tin. Chờ admin duyệt để kích hoạt tín hiệu.")

    return "OK", 200
