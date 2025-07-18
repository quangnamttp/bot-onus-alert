from flask import request
import json
from config import PENDING_USERS_PATH
from services.message_sender import send_message  # phản hồi tin nhắn

def handle_webhook():
    # 📡 Facebook gọi GET lần đầu để xác minh Webhook
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == "cofure_verify_2025":
            return challenge, 200
        return "❌ Sai verify token", 403

    # 📦 Bắt payload POST từ người dùng Messenger
    data = request.get_json()
    print("📦 Full JSON nhận được:\n", json.dumps(data, indent=2))

    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):
            sender_id = msg.get("sender", {}).get("id")
            if not sender_id:
                print("❌ Không tìm thấy sender.id")
                continue

            print(f"🆔 PSID nhận được: {sender_id}")
            message_text = msg.get("message", {}).get("text", "")
            if message_text:
                print(f"💬 Tin nhắn: {message_text}")
            else:
                print("⚠️ Không có nội dung text")

            # 📂 Ghi vào pending_users.json
            try:
                with open(PENDING_USERS_PATH, "r") as f:
                    pending = json.load(f)
            except Exception:
                pending = []

            if sender_id not in pending:
                pending.append(sender_id)
                with open(PENDING_USERS_PATH, "w") as f:
                    json.dump(pending, f, indent=2)
                print("⏳ Ghi vào pending_users.json")
            else:
                print("🔁 PSID đã tồn tại")

            # 📨 Gửi phản hồi ngay qua Messenger
            send_message(sender_id, "✅ Cofure đã nhận tin nhắn của bạn!")

    return "ok", 200
