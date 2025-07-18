import json
import os
from config import USER_REGISTRY_PATH
from messenger.message_sender import send_message

def xac_nhan_user(sender_id):
    # Đảm bảo file tồn tại
    if not os.path.exists(USER_REGISTRY_PATH):
        with open(USER_REGISTRY_PATH, "w") as f:
            json.dump([], f)

    # Đọc danh sách đã duyệt
    try:
        with open(USER_REGISTRY_PATH, "r") as f:
            registry = json.load(f)
    except Exception:
        registry = []

    if sender_id in registry:
        send_message(sender_id, "✅ Bạn đã được duyệt!")
    else:
        # 📩 Gắn link trực tiếp trên tên người
        send_message(
            sender_id,
            "⚠️ Bạn chưa được duyệt.\n📩 Vui lòng liên hệ admin [Trương Tấn Phương](https://www.facebook.com/quangnamttp)"
        )
