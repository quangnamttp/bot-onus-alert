from messenger.registry_manager import get_user_status, update_user_status

def check_toggle_request(user_id, message_text):
    status = get_user_status(user_id)
    if not status or not status.get("approved"):
        return None  # ❌ Nếu chưa được duyệt thì không xử lý tín hiệu

    msg = message_text.strip().lower()

    # 🔕 Tắt tín hiệu
    if msg in ["tắt tín hiệu", "ngưng tín hiệu", "stop"]:
        update_user_status(user_id, "signal_active", False)
        return "🚫 Bạn đã tắt tín hiệu ONUS. Không còn nhận bản tin mỗi ngày."

    # 🔔 Bật lại tín hiệu
    if msg in ["bật tín hiệu lại", "kích hoạt tín hiệu", "start"]:
        update_user_status(user_id, "signal_active", True)
        return "✅ Tín hiệu ONUS đã được bật lại! Bạn sẽ nhận bản tin mỗi ngày."

    return None  # ❌ Không khớp lệnh bật/tắt
