from messenger.send_message import send_message, send_quick_reply

ADMIN_ID = "24110537551888914"  # ← ID admin thực của bạn
DUYET_OK = "✅ Bạn đã được xét duyệt! Tín hiệu sẽ gửi mỗi ngày."
TUCHOI_MSG = "❌ Yêu cầu bị từ chối. Bạn có thể thử lại sau."

def handle_new_message(user_id, user_name, message_text):
    # ✅ Nếu là phản hồi nút (Quick Reply)
    if isinstance(message_text, dict):
        payload = message_text.get("quick_reply", {}).get("payload")
        if payload:
            if payload.startswith("DANGKY_"):
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
                send_message(user_id, "🛑 Bạn đã từ chối đăng ký nhận tín hiệu. Có thể thử lại sau nhé!")
            elif payload.startswith("DUYET_"):
                target_id = payload.split("_")[1]
                send_message(target_id, DUYET_OK)
                send_message(user_id, f"📬 Đã duyệt người dùng {target_id}.")
            elif payload.startswith("TUCHOI_"):
                target_id = payload.split("_")[1]
                send_message(target_id, TUCHOI_MSG)
                send_message(user_id, f"🛑 Đã từ chối người dùng {target_id}.")
            return  # ✅ xử lý xong rồi, không gửi chào lại

    # ✅ Nếu là tin nhắn văn bản bình thường → gửi chào với nút
    send_quick_reply(
        user_id,
        "Chào bạn 👋 Mình là Cofure — trợ lý tín hiệu ONUS.\nBạn có muốn nhận bản tin mỗi ngày không?",
        [
            { "content_type": "text", "title": "✅ Đăng ký nhận", "payload": f"DANGKY_{user_id}" },
            { "content_type": "text", "title": "❌ Không nhận", "payload": f"HUY_{user_id}" }
        ]
    )
