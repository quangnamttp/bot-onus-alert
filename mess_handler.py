import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")

# Load admin PSID từ file cấu hình
def get_admin_psid():
    with open("admin_config.json", "r") as f:
        return json.load(f)["admin_psid"]

# Gửi tin nhắn qua Messenger
def send_message(recipient_id, message_text):
    if not recipient_id:
        print("❌ Thiếu recipient_id")
        return

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={FB_PAGE_TOKEN}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    print(f"📨 Gửi đến {recipient_id}: {response.status_code} — {response.text}")

# Lưu PSID vào pending nếu chưa duyệt
def save_pending_user(psid):
    try:
        with open("pending_users.json", "r") as f:
            pending = json.load(f)
    except:
        pending = []

    if psid not in pending:
        pending.append(psid)
        with open("pending_users.json", "w") as f:
            json.dump(pending, f)
        print("🕒 Đã ghi vào pending:", psid)
        send_message(get_admin_psid(), f"📩 Có user mới nhắn vào Page:\nID: {psid}\nGửi /duyet {psid} để kích hoạt bot.")

# Duyệt user từ admin
def approve_user(psid):
    with open("user_registry.json", "r") as f:
        users = json.load(f)
    if psid not in users:
        users.append(psid)
        with open("user_registry.json", "w") as f:
            json.dump(users, f)
        print("✅ Đã duyệt user:", psid)
        send_message(psid, "🎉 Bot Cofure đã được kích hoạt cho bạn!")

    # Xóa khỏi pending
    with open("pending_users.json", "r") as f:
        pending = json.load(f)
    if psid in pending:
        pending.remove(psid)
        with open("pending_users.json", "w") as f:
            json.dump(pending, f)

# Xử lý Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 Webhook nhận:", json.dumps(data))

    try:
        messaging_event = data["entry"][0]["messaging"][0]
        sender_id = messaging_event["sender"]["id"]
        message_text = messaging_event["message"].get("text", "")

        # Nếu là admin và gửi lệnh duyệt
        if sender_id == get_admin_psid() and message_text.startswith("/duyet "):
            psid_to_approve = message_text.split("/duyet ")[1].strip()
            approve_user(psid_to_approve)
            return "OK", 200

        # Nếu là user thường → lưu vào pending
        save_pending_user(sender_id)
        send_message(sender_id, "🤖 Bot Cofure đã nhận tin. Chờ admin duyệt để kích hoạt tín hiệu!")

    except Exception as e:
        print("❌ Lỗi xử lý webhook:", str(e))

    return "OK", 200

# Khởi động bot
if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))
