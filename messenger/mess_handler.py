from flask import request
import json
import os
from config import PENDING_USERS_PATH
from messenger.message_sender import send_message  # dùng đúng nhánh

def handle_webhook():
    # 📡 Xác minh Webhook từ Facebook (GET)
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == "cofure_verify_2025":
            return challenge, 200
        return "❌ Verify token sai", 403

    # 📦 Xử lý payload POST từ Messenger (người dùng gửi tin)
    data = request.get_json()
    print("📦 Full JSON nhận được:\n", json.dumps(data, indent=2))

    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):
            # ⚠️ Bỏ qua tin nhắn do bot gửi (tránh phản hồi lặp)
            if msg.get("message", {}).get("is_echo"):
                print("🔁 Bỏ qua tin nhắn do bot gửi")
                continue

            sender_id = msg.get("sender", {}).get("id")
            if not sender_id:
                print("❌ Không tìm thấy sender.id")
                continue

            print(f"🆔 PSID nhận được: {sender_id}")
            message_text = msg.get("message", {}).get("text", "")
            print(f"💬 Tin nhắn: {message_text}" if message_text else "⚠️ Không có nội dung text")

            # 📂 Ghi PSID vào file pending_users.json nếu chưa có
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
                print("⏳ Đã ghi vào pending_users.json")
            else:
                print("🔁 PSID đã tồn tại")

            # 📨 Gửi phản hồi tới Messenger 1 lần duy nhất
            send_message(sender_id, "✅ Cofure đã nhận tín hiệu của bạn!")

    return "ok", 200
