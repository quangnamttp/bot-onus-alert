from messenger.message_sender import send_message
from messenger.registry_manager import get_all_registered_users
from utils.signal_tracker import get_today_stats

def send_summary():
    stats = get_today_stats()
    message = f"""📊 Báo cáo cuối ngày từ Cofure

🧮 Tổng số tín hiệu: {stats['total']}
📈 Tỷ lệ Long/Short: {stats['long']}/{stats['short']}
🧠 Trung bình R:R: {stats['avg_rr']}

🌙 Chúc bạn nghỉ ngơi tốt để chuẩn bị cho ngày mai 🔁
"""
    users = get_all_registered_users()
    for psid in users:
        send_message(psid, message)
