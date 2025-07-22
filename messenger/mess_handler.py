from messenger.registry_manager import register_user, get_user_status
from messenger.signal_toggle import check_toggle_request
from utils.vnđ_formatter import format_vnd 
def handle_new_message(user_id, user_name, message_text):
    status = get_user_status(user_id)
    if not status:
        register_user(user_id, user_name)
        return {
            "text": f"Chào bạn 👋 Mình là Cofure — trợ lý gửi tín hiệu giao dịch thị trường ONUS.\n"
                    f"Bạn có muốn nhận bản tin & tín hiệu mỗi ngày không ạ?",
            "quick_replies": ["✅ Đồng ý", "❌ Từ chối"]
        }

    # Check if message is toggle request
    toggle_response = check_toggle_request(user_id, message_text)
    if toggle_response:
        return { "text": toggle_response }

    # Default fallback
    return { "text": "Bạn đã đăng ký rồi nha 😊 Nếu cần tắt/bật tín hiệu có thể nhắn: “Tắt tín hiệu” hoặc “Bật tín hiệu lại”." }
