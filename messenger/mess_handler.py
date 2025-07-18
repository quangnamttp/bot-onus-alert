from flask import request
import json
import os

def handle_webhook():
    data = request.get_json()

    # 📦 Log toàn bộ payload JSON
    print("📦 Full JSON nhận được:\n", json.dumps(data, indent=2))

    for entry in data.get("entry", []):
        for messaging_event in entry.get("messaging", []):
            # 🆔 Trích PSID từ payload
            if "sender" in messaging_event and "id" in messaging_event["sender"]:
                sender_id = messaging_event["sender"]["id"]
                print(f"🆔 PSID nhận được: {sender_id}")
            else:
                print("❌ Không tìm thấy sender.id")
                continue

            # 💬 Log nội dung tin nhắn nếu có
            message_text = messaging_event.get("message", {}).get("text", "")
            if message_text:
                print(f"💬 Tin nhắn: {message_text}")
            else:
                print("⚠️ Tin nhắn không có text")

            # 📂 Ghi vào pending_users.json nếu chưa có
            pending_path = os.path.join("data", "pending_users.json")
            try:
                with open(pending_path, "r") as f:
                    pending_users = json.load(f)
            except Exception:
                pending_users = []

            if sender_id not in pending_users:
                pending_users.append(sender_id)
                with open(pending_path, "w") as f:
                    json.dump(pending_users, f, indent=2)
                print("⏳ Đã ghi vào pending_users.json")
            else:
                print("🔁 PSID đã tồn tại trong pending_users.json")

    return "ok", 200
