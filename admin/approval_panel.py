from messenger.registry_manager import get_user_status, update_user_status

def approve_user(user_id):
    user = get_user_status(user_id)
    if not user:
        return f"❌ Không tìm thấy user {user_id} để duyệt."
    
    update_user_status(user_id, "approved", True)
    update_user_status(user_id, "signal_active", True)
    return f"✅ User {user_id} đã được xét duyệt và bắt đầu nhận tín hiệu."

def check_status(user_id):
    user = get_user_status(user_id)
    if not user:
        return f"🔍 User {user_id} chưa từng đăng ký."

    name = user.get("name", "Không rõ")
    status = "Đã duyệt ✅" if user.get("approved") else "Chưa duyệt ❌"
    signal = "Đang nhận tín hiệu 📡" if user.get("signal_active") else "Đã tắt tín hiệu 🔕"

    return f"👤 {name} | {user_id}\n• Trạng thái: {status}\n• Nhận tín hiệu: {signal}"
