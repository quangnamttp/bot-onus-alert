from messenger.message_sender import send_message
from messenger.registry_manager import is_registered, mark_registered
from utils.mid_tracker import has_processed, mark_processed

def handle_message(event):
    sender_id = event['sender']['id']
    message_text = event['message'].get('text', '').strip().lower()
    mid = event['message'].get('mid', '')

    if has_processed(mid):
        return
    mark_processed(mid)

    # Nếu user đã kích hoạt → bot xử lý gửi lệnh theo scheduler
    if is_registered(sender_id):
        return

    # Nếu user nhắn lần đầu → hỏi xác nhận
    if message_text in ["", "hi", "hello", "chào", "bắt đầu", "start"] or len(message_text) < 5:
        send_message(sender_id,
            "👋 Chào bạn! Peace là bot gửi tín hiệu trade kỹ thuật từ 06:00 đến 23:00 mỗi ngày theo sàn ONUS.\n📈 Bạn có muốn nhận tín hiệu không?\n🟩 Trả lời 'Có' để kích hoạt bot\n⬜ Trả lời 'Không' để thoát"
        )
        return

    # Nếu user chọn “Có” → kích hoạt + ghi PSID
    if message_text == "có":
        mark_registered(sender_id)
        send_message(sender_id,
            "✅ Peace đã được kích hoạt cho bạn! Tín hiệu crypto sẽ bắt đầu gửi từ phiên sáng lúc 06:00 hàng ngày 💹"
        )
        return

    # Nếu user chọn “Không” → bot giữ im lặng
    if message_text == "không":
        return

    return
