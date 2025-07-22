from messenger.registry_manager import load_user_status, is_approved_and_active

def broadcast_message(text):
    user_data = load_user_status()
    for user_id in user_data:
        if is_approved_and_active(user_id):
            send_message(user_id, text)

def send_message(user_id, message):
    # Hàm gửi tin qua Messenger API — bạn thay bằng hàm thực tế
    print(f"[broadcast] → {user_id}: {message}")

def broadcast_alert(level, content):
    emoji = "⚠️" if level == "warning" else "✅"
    full_msg = f"{emoji} THÔNG BÁO TỪ HỆ THỐNG:\n{content}"
    broadcast_message(full_msg)
