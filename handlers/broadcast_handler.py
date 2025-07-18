import json
import os
from config import USER_REGISTRY_PATH
from messenger.message_sender import send_message

def broadcast_message(sender_id, message_text):
    parts = message_text.strip().split(" ", 1)
    if len(parts) < 2 or parts[0].lower() != "/broadcast":
        send_message(sender_id, "❌ Sai cú pháp. Dùng: /broadcast [nội dung tin]")
        return

    broadcast_text = parts[1]

    if not os.path.exists(USER_REGISTRY_PATH):
        send_message(sender_id, "⚠️ Chưa có user nào được duyệt để nhận bản tin.")
        return

    try:
        with open(USER_REGISTRY_PATH, "r") as f:
            registry = json.load(f)
    except Exception as e:
        print("❌ Lỗi đọc user_registry.json:", e)
        registry = []

    count = 0
    for psid in registry:
        send_message(psid, broadcast_text)
        count += 1

    send_message(sender_id, f"✅ Đã gửi tới {count} người dùng được duyệt.")
