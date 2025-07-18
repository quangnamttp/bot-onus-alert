from flask import request, jsonify
import json
import os

def handle_webhook():
    data = request.get_json()
    print("📥 Payload từ Messenger:", data)

    for entry in data.get("entry", []):
        for messaging_event in entry.get("messaging", []):
            # 🆔 Lấy PSID người gửi
            sender_id = messaging_event["sender"]["id"]
            print(f"🆔 PSID nhận được: {sender_id}")

            # 💬 Lấy nội dung tin nhắn (nếu có)
            if "message" in messaging_event:
                message_text = messaging_event["message"].get("text", "")
                print(f"💬 Tin nhắn: {message_text}")

                # ✅ Ghi vào pending_users.json nếu chưa có
                pending_path = os.path.join("data", "pending_users.json")
                try:
                    with open(pending_path, "r") as f:
                        pending_users = json.load(f)
                except:
                    pending_users = []

                if sender_id not in pending_users:
                    pending_users.append(sender_id)
                    with open(pending_path, "w") as f:
                        json.dump(pending_users, f, indent=2)
                    print("⏳ Đã ghi vào pending_users.json")

            # ❗ Nếu muốn xử lý lệnh /duyet, /huy → tách riêng ở handler khác

    return "ok", 200
