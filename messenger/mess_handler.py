from flask import request
import json
import os
from config import PENDING_USERS_PATH
from messenger.message_sender import send_message  # Đúng nhánh nếu nằm trong messenger/

def handle_webhook():
    # 🔒 Xác minh webhook từ Facebook (GET)
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == "cofure_verify_2025":
            return challenge, 200
        return "❌ Verify token sai", 403

    # 📨 Payload POST từ người dùng Messenger
    data = request.get_json()
    print("📦 Payload nhận được:\n", json.dumps(data, indent=2))

    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):
            message_obj = msg.get("message", {})

            # ⚠️ Bỏ qua tin nhắn echo do bot tự gửi
            if message_obj.get("is_echo"):
                print("🔁 Bỏ qua tin nhắn echo từ bot")
                continue

            # ⚠️ Bỏ qua nếu không phải text (ảnh, sticker,…)
            if "text" not in message_obj:
                print("⚠️ Không có nội dung text — bỏ qua")
                continue

            sender_id = msg.get("sender", {}).get("id")
            if not sender_id:
                print("❌ Không tìm thấy sender.id")
                continue

            message_text = message_obj.get("text", "")
            print(f"🆔 PSID: {sender_id}")
            print(f"💬 Nội dung: {message_text}")

            # 📂 Kiểm tra và ghi PSID nếu chưa có
            if not os.path.exists(PENDING_USERS_PATH):
                with open(PENDING_USERS_PATH, "w") as f:
                    json.dump([], f)

            try:
                with open(PENDING_USERS_PATH, "r") as f:
                    pending = json.load(f)
            except Exception as e:
                print("❌ Lỗi đọc pending_users.json:", e)
                pending = []

            if sender_id not in pending:
                pending.append(sender_id)
                with open(PENDING_USERS_PATH, "w") as f:
                    json.dump(pending, f, indent=2)
                print("⏳ Ghi PSID vào pending_users.json")
            else:
                print("🔁 PSID đã tồn tại")

            # ✅ Gửi phản hồi một lần duy nhất
            send_message(sender_id, "✅ Cofure đã nhận tín hiệu của bạn!")

    return "ok", 200
