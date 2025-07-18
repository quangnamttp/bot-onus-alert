from flask import request
import json
import os
from config import PENDING_USERS_PATH
from messenger.message_sender import send_message

# 👉 Import các module nâng cấp
from handlers.duyet_handler import duyet_user
from handlers.xacnhan_handler import xac_nhan_user
from handlers.broadcast_handler import broadcast_message
from utils.mid_tracker import is_mid_processed, mark_mid_processed
from utils.permissions import is_admin

def handle_webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == "cofure_verify_2025":
            return challenge, 200
        return "❌ Verify token sai", 403

    data = request.get_json()
    print("📦 Payload nhận được:\n", json.dumps(data, indent=2))

    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):
            message_obj = msg.get("message", {})
            if message_obj.get("is_echo"):
                print("🔁 Bỏ qua tin nhắn echo từ bot")
                continue

            if "text" not in message_obj:
                print("⚠️ Không có nội dung text — bỏ qua")
                continue

            mid = message_obj.get("mid")
            if not mid or is_mid_processed(mid):
                print(f"🔁 Payload {mid} đã xử lý — bỏ qua")
                continue
            mark_mid_processed(mid)

            sender_id = msg.get("sender", {}).get("id")
            if not sender_id:
                print("❌ Không tìm thấy sender.id")
                continue

            message_text = message_obj.get("text", "").strip()
            print(f"🆔 PSID: {sender_id}")
            print(f"💬 Nội dung: {message_text}")

            # ✅ Lệnh quản trị: chỉ admin mới dùng được
            if message_text.startswith("/duyet"):
                if not is_admin(sender_id):
                    send_message(sender_id, "⛔ Bạn không có quyền duyệt người dùng.")
                    continue
                duyet_user(sender_id, message_text)
                continue

            if message_text.lower().startswith("/broadcast"):
                if not is_admin(sender_id):
                    send_message(sender_id, "⛔ Bạn không có quyền gửi bản tin.")
                    continue
                broadcast_message(sender_id, message_text)
                continue

            # ✅ Lệnh người dùng: kiểm tra trạng thái duyệt
            if message_text.lower().startswith("/xacnhan"):
                xac_nhan_user(sender_id)
                continue

            # 📂 Ghi vào pending_users.json nếu chưa có
            if not os.path.exists(PENDING_USERS_PATH):
                with open(PENDING_USERS_PATH, "w") as f:
                    json.dump([], f)

            try:
                with open(PENDING_USERS_PATH, "r") as f:
                    pending = json.load(f)
            except Exception:
                pending = []

            if sender_id not in pending:
                pending.append(sender_id)
                with open(PENDING_USERS_PATH, "w") as f:
                    json.dump(pending, f, indent=2)
                print("⏳ Ghi PSID vào pending_users.json")
            else:
                print("🔁 PSID đã tồn tại")

            # ✅ Phản hồi mặc định cho tin nhắn bình thường
            send_message(sender_id, "✅ Cofure đã nhận tín hiệu của bạn!")

    return "ok", 200
