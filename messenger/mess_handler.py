from messenger.send_message import send_message, send_quick_reply

ADMIN_ID = "24110537551888914"  # ← ID của bạn, Trương

def handle_new_message(user_id, user_name, message_text):
    if isinstance(message_text, str):
        # Tin chào với nút đăng ký
        send_quick_reply(
            user_id,
            "Chào bạn 👋 Mình là Cofure — trợ lý tín hiệu ONUS.\nBạn muốn nhận bản tin mỗi ngày chứ?",
            [
                { "content_type": "text", "title": "✅ Đăng ký nhận", "payload": f"DANGKY_{user_id}" },
                { "content_type": "text", "title": "❌ Không nhận", "payload": f"HUY_{user_id}" }
            ]
        )
        return

    payload = message_text.get("quick_reply", {}).get("payload")

    # Xử lý đăng ký
    if payload and payload.startswith("DANGKY_"):
        target_id = payload.split("_")[1]
        send_message(user_id, "📨 Yêu cầu đã gửi đến admin. Vui lòng chờ xét duyệt.")
        send_quick_reply(
            ADMIN_ID,
            f"👤 Người dùng {target_id} muốn nhận tín hiệu ONUS.\nBạn duyệt chứ?",
            [
                { "content_type": "text", "title": "✅ Duyệt", "payload": f"DUYET_{target_id}" },
                { "content_type": "text", "title": "❌ Từ chối", "payload": f"TUCHOI_{target_id}" }
            ]
        )

    # Từ chối đăng ký
    elif payload and payload.startswith("HUY_"):
        send_message(user_id, "🛑 Bạn đã từ chối nhận tín hiệu. Có thể đăng ký sau nhé!")

    # Admin duyệt
    elif payload and payload.startswith("DUYET_"):
        target_id = payload.split("_")[1]
        send_message(target_id, "✅ Bạn đã được xét duyệt! Tín hiệu sẽ được gửi mỗi ngày.")
        send_message(user_id, f"📬 Đã duyệt người dùng {target_id}.")

    # Admin từ chối
    elif payload and payload.startswith("TUCHOI_"):
        target_id = payload.split("_")[1]
        send_message(target_id, "❌ Yêu cầu bị từ chối. Thử lại sau nhé!")
        send_message(user_id, f"🛑 Đã từ chối người dùng {target_id}.")
