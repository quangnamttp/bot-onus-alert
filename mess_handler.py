from flask import request, jsonify
import json
import os

def handle_webhook():
    # 🌐 Nhận payload JSON từ Messenger
    data = request.get_json()

    # 📦 Log toàn bộ payload để debug
    print("📦 Full JSON nhận được:\n", json.dumps(data, indent=2))

    for entry in data.get("entry", []):
        for messaging_event in entry.get("messaging", []):
            # ✅ Kiểm tra tồn tại trường sender
            if "sender" in messaging_event and "id" in messaging_event["sender"]:
                sender_id = messaging_event["sender"]["id"]
                print(f"🆔 PSID nhận được: {sender_id}")
            else:
                print("❌ Không tìm thấy sender.id trong payload")
                continue

            # 💬 Log nội dung tin nhắn nếu có
            if "message" in messaging_event and "text" in messaging_event["message"]:
                message_text = messaging_event["message"]["text"]
                print(f"💬 Tin nhắn: {message_text}")
            else:
                print("⚠️ Tin nhắn không có nội dung text")
                message_text = ""

            # ✅ Ghi PSID vào file pending nếu chưa có
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
            else:
                print("🔁 PSID đã tồn tại trong pending_users.json")

    return "ok", 200
