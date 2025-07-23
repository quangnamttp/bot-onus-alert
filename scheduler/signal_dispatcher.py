from core.signal_generator import generate_signals
from messages.format_signal import format_signal_batch
from messenger.registry_manager import load_user_status, is_approved_and_active
from messenger.send_message import send_message  # ✅ Gửi tin thật qua Messenger API

# ✅ Gửi tín hiệu batch cho người dùng đã duyệt & còn bật tín hiệu
def send_regular_signals():
    signals = generate_signals()  # 📦 List lệnh trade từ logic kỹ thuật
    msg = format_signal_batch(signals)  # 💬 Format thành tin nhắn đẹp, dễ hiểu

    users = load_user_status()
    for user_id, info in users.items():
        if is_approved_and_active(user_id):
            send_message(user_id, msg)  # ✅ Gửi tin qua hàm gửi thật
