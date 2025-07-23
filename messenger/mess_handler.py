from messenger.registry_manager import (
    register_user,
    get_user_status,
    update_user_status,
    approve_user,
)
from messenger.signal_toggle import check_toggle_request
from messenger.send_message import send_message

# 📌 ID Messenger cá nhân của bạn — để bot gửi xét duyệt riêng
ADMIN_ID = "100036886332606"  # ← Đã chuẩn

def handle_new_message(user_id, user_name, message_text):
    # 🔍 Kiểm tra trạng thái người dùng
    status = get_user_status(user_id)

    # 🟢 Nếu là user mới — đăng ký ban đầu
    if not status:
        register_user(user_id, user_name)
        reply = (
            "Chào bạn 👋 Mình là Cofure — trợ lý gửi tín hiệu giao dịch thị trường ONUS.\n"
            "Bạn có muốn nhận bản tin & tín hiệu mỗi ngày không?\n"
            "👉 Nếu đồng ý, hãy nhắn: “✅ Đồng ý”"
        )
        send_message(user_id, reply)
        return

    # 🛑 Nếu chưa được xét duyệt → chỉ phản hồi 1 lần
    if not status.get("approved"):
        fallback = (
            "Bạn chưa được xét duyệt để nhận tín hiệu.\n"
            "Vui lòng chờ xét duyệt từ [Trương Tấn Phương](https://www.facebook.com/quangnamttp) nhé ✅"
        )
        send_message(user_id, fallback)
        return

    # ✅ Người dùng nhắn “Đồng ý” → gửi yêu cầu xét duyệt đến bạn
    if message_text.strip() == "✅ Đồng ý":
        send_message(user_id,
            "📨 Yêu cầu của bạn đã được gửi đến [Trương Tấn Phương](https://www.facebook.com/quangnamttp) để xét duyệt."
        )
        send_message(ADMIN_ID,
            f"👤 Người dùng {user_id} vừa nhấn ✅ Đồng ý.\n"
            f"Gõ: Duyệt {user_id} hoặc Từ chối {user_id} để xử lý."
        )
        return

    # 🎯 Admin duyệt: “Duyệt <user_id>”
    if message_text.startswith("Duyệt "):
        target_id = message_text.split("Duyệt ")[1].strip()
        approve_user(target_id)
        send_message(target_id,
            "✅ [Trương Tấn Phương](https://www.facebook.com/quangnamttp) đã xét duyệt bạn!\n"
            "Tín hiệu ONUS sẽ được gửi tại đây qua Messenger mỗi ngày."
        )
        send_message(user_id, f"✅ Đã xét duyệt cho {target_id}.")
        return

    # ❌ Admin từ chối: “Từ chối <user_id>”
    if message_text.startswith("Từ chối "):
        target_id = message_text.split("Từ chối ")[1].strip()
        send_message(target_id,
            "❌ Bạn chưa được xét duyệt để nhận tín hiệu.\n"
            "Vui lòng liên hệ [Trương Tấn Phương](https://www.facebook.com/quangnamttp) nếu cần hỗ trợ."
        )
        send_message(user_id, f"🚫 Đã từ chối yêu cầu của {target_id}.")
        return

    # 🔁 Bật/tắt tín hiệu nếu có
    toggle_response = check_toggle_request(user_id, message_text)
    if toggle_response:
        send_message(user_id, toggle_response)
        return

    # ✅ Nếu đã được duyệt mà không khớp lệnh nào → giữ im lặng hoặc phản hồi nhẹ
    send_message(user_id, "🤖 Mình đã ghi nhận tin nhắn. Bạn đã được xét duyệt rồi!")
