from marketdata.futures_tracker import get_top_coin_data
from messages.greeting_format import format_morning_greeting
from messenger.registry_manager import load_user_status, is_approved_and_active

def send_morning_report():
    user_data = load_user_status()
    for user_id, info in user_data.items():
        if is_approved_and_active(user_id):
            coin_data = get_top_coin_data()
            message = format_morning_greeting(info["name"], coin_data)
            send_message(user_id, message)

def send_message(user_id, message):
    # Đây là hàm gửi tin qua Messenger API → bạn có thể thay bằng hàm thực tế
    print(f"[morning_report] → {user_id}: {message}")
