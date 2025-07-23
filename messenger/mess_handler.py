import json
import os
from messenger.send_message import send_message, send_quick_reply

ADMIN_ID = "24110537551888914"
APPROVED_FILE = "data/approved_users.json"

# ✅ Tải danh sách đã duyệt từ file
def load_approved_users():
    if not os.path.exists(APPROVED_FILE):
        return set()
    try:
        with open(APPROVED_FILE, "r") as f:
            return set(json.load(f))
    except Exception:
        return set()

# ✅ Lưu danh sách đã duyệt vào file
def save_approved_users(user_set):
    with open(APPROVED_FILE, "w") as f:
        json.dump(list(user_set), f)

# ✅ Xử lý tin nhắn từ Messenger
def handle_new_message(user_id, user_name, message_text):
    approved_users = load_approved_users()

    # Nếu là phản hồi từ nút bấm Quick Reply
    if isinstance(message_text, dict):
        payload = message_text.get("quick_reply", {}).get("payload")
        if payload:
            if payload.startswith("DANGKY_"):
                if user_id in approved_users:
                    send_message(user_id, "🔁 Bạn đã đăng ký nhận tín hiệu ONUS rồi. Không cần đăng ký lại.")
                else:
                    send_message(user_id, "📨 Yêu cầu đã được gửi tới admin để xét duyệt.")
                    send_quick_reply(
                        ADMIN_ID,
                        f"👤 Người dùng {user_id} muốn nhận tín hiệu ONUS.\nBạn duyệt không?",
                        [
                            { "content_type": "text", "title": "✅ Duyệt", "payload": f"DUYET_{user_id}" },
                            { "content_type": "text", "title": "❌ Từ chối", "payload": f"TUCHOI_{user_id}" }
                        ]
                    )

            elif payload.startswith("HUY_"):
                send_message(user_id, "🛑 Bạn đã từ chối nhận tín hiệu. Có thể thử lại sau nhé!")

            elif payload.startswith("DUYET_"):
                target_id = payload.split("_")[1]
                if target_id in approved_users:
                    send_message(user_id, f"🔁 Người dùng {target_id} đã được duyệt trước đó.")
                else:
                    approved_users.add(target_id)
                    save_approved_users(approved_users)
                    send_message(target_id, "✅ Bạn đã được admin xét duyệt! Tín hiệu sẽ gửi mỗi ngày.")
                    send_message(user_id, f"📬 Đã duyệt người dùng {target_id}.")

            elif payload.startswith("TUCHOI_"):
                target_id = payload.split("_")[1]
                send_message(target_id, "❌ Yêu cầu bị từ chối. Bạn có thể thử lại sau.")
                send_message(user_id, f"🛑 Đã từ chối người dùng {target_id}.")
            return  # ✅ Không lặp lại tin chào

    # Nếu là tin nhắn văn bản bình thường → gửi lời chào kèm nút
    send_quick_reply(
        user_id,
        "Chào bạn 👋 Mình là Cofure — trợ lý tín hiệu ONUS.\nBạn có muốn nhận bản tin mỗi ngày không?",
        [
            { "content_type": "text", "title": "✅ Đăng ký nhận", "payload": f"DANGKY_{user_id}" },
            { "content_type": "text", "title": "❌ Không nhận", "payload": f"HUY_{user_id}" }
        ]
    )
