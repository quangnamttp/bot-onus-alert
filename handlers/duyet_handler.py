import json
import os
from config import USER_REGISTRY_PATH
from messenger.message_sender import send_message

def duyet_user(sender_id, message_text):
    parts = message_text.strip().split()
    if len(parts) != 2 or parts[0].lower() != "/duyet":
        send_message(sender_id, "❌ Sai cú pháp. Dùng: /duyet [PSID]")
        return

    target_psid = parts[1]

    # Tạo file user_registry.json nếu chưa tồn tại
    if not os.path.exists(USER_REGISTRY_PATH):
        with open(USER_REGISTRY_PATH, "w") as f:
            json.dump([], f)

    # Đọc danh sách đã duyệt
    try:
        with open(USER_REGISTRY_PATH, "r") as f:
            registry = json.load(f)
    except Exception as e:
        print("❌ Lỗi đọc user_registry.json:", e)
        registry = []

    # Duyệt nếu chưa có
    if target_psid not in registry:
        registry.append(target_psid)
        with open(USER_REGISTRY_PATH, "w") as f:
            json.dump(registry, f, indent=2)
        send_message(sender_id, f"✅ Đã duyệt PSID: {target_psid}")
    else:
        send_message(sender_id, f"⚠️ PSID {target_psid} đã được duyệt trước đó")
