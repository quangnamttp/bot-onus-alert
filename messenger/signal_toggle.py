from messenger.registry_manager import update_user_status, get_user_status

TOGGLE_OFF_WORDS = ["tắt tín hiệu", "stop", "không nhận nữa", "nghỉ", "tạm nghỉ"]
TOGGLE_ON_WORDS = ["bật tín hiệu", "nhận lại", "mở tín hiệu", "kích hoạt", "bật lại"]

def check_toggle_request(user_id, message_text):
    msg = message_text.strip().lower()

    if any(w in msg for w in TOGGLE_OFF_WORDS):
        update_user_status(user_id, "signal_active", False)
        return "Đã ghi nhận yêu cầu của bạn. Tín hiệu sẽ được tạm dừng gửi từ bây giờ nha!"

    if any(w in msg for w in TOGGLE_ON_WORDS):
        user = get_user_status(user_id)
        if user and user.get("approved"):
            update_user_status(user_id, "signal_active", True)
            return "Bạn đã bật lại chế độ nhận tín hiệu rồi nha!"
        else:
            return "Bạn chưa được duyệt để nhận tín hiệu. Vui lòng chờ xét duyệt từ admin nhé."

    return None
