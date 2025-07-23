from messenger.registry_manager import (
    register_user,
    get_user_status,
    update_user_status,
    approve_user,
)
from messenger.signal_toggle import check_toggle_request
from messenger.send_message import send_message

ADMIN_ID = "100036886332606"  # ← Messenger ID của bạn

def handle_new_message(user_id, user_name, message_text):
    status = get_user_status(user_id)

    # 🟢 User mới → đăng ký
    if not status:
        register_user(user_id, user_name)
        reply = (
            "Chào bạn 👋 Mình là Cofure — trợ lý gửi tín hiệu giao dịch thị trường ONUS.\n"
            "Bạn có muốn nhận bản tin & tín hiệu mỗi ngày không?\n"
            "👉 Nếu đồng ý, hãy nhắn: “✅ Đồng ý”"
        )
        send_message(user_id, reply)
        return

    # ✅ User nhấn “Đồng ý” → gửi xét duyệt cho admin
    if message_text.strip() == "✅ Đồng ý":
        send_message(user_id,
            "📨 Yêu cầu của bạn đã được gửi tới admin để xét duyệt.\n"
            "Vui lòng đợi admin Trương Tấn Phương xác nhận yêu cầu của bạn."
        )
        print(f"[XétDuyệt] Gửi xét duyệt đến ADMIN_ID: {ADMIN_ID}")
        send_message(ADMIN_ID,
            f"👤 Người dùng {user_id} vừa nhấn ✅ Đồng ý.\n"
            f"Gõ: Duyệt {user_id} hoặc Từ chối {user_id} để xử lý."
        )
        return

    # 🎯 Admin duyệt user
    if message_text.startswith("Duyệt "):
        target_id = message_text.split("Duyệt ")[1].strip()
        approve_user(target_id)
        send_message(target_id,
            "✅ Trương Tấn Phương đã xét duyệt bạn!\n"
            "Tín hiệu ONUS sẽ được gửi tại đây qua Messenger mỗi ngày."
        )
        send_message(user_id, f"✅ Đã xét duyệt cho {target_id}.")
        return

    # ❌ Admin từ chối user
    if message_text.startswith("Từ chối "):
        target_id = message_text.split("Từ chối ")[1].strip()
        send_message(target_id,
            "❌ Bạn chưa được xét duyệt để nhận tín hiệu.\n"
            "Vui lòng đợi admin Trương Tấn Phương xác nhận lại sau."
        )
        send_message(user_id, f"🚫 Đã từ chối yêu cầu của {target_id}.")
        return

    # 🔁 Bật/tắt tín hiệu
    toggle_response = check_toggle_request(user_id, message_text)
    if toggle_response:
        send_message(user_id, toggle_response)
        return

    # ✅ Nếu đã được duyệt → phản hồi nhẹ
    if status.get("approved"):
        send_message(user_id, "🤖 Bạn đã được xét duyệt rồi, tín hiệu ONUS sẽ tiếp tục được gửi mỗi ngày.")
        return

    # 🛑 Nếu chưa duyệt và không phải “✅ Đồng ý” → KHÔNG gửi tin gì
    return
