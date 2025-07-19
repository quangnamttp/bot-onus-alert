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

    if is_registered(sender_id):
        send_message(sender_id, "✅ Bot Cofure đã bật cho bạn! Tín hiệu sẽ gửi theo từng khung giờ 🚀")
        return

    if message_text in ["", "hi", "hello", "chào", "bắt đầu", "start"] or len(message_text) < 5:
        send_message(sender_id,
            "👋 Chào bạn! Đây là bot Cofure gửi tín hiệu trade từ 00:00 đến 23:59.\n🧠 Bạn có muốn nhận tín hiệu không?\n🟩 Trả lời 'Có' để kích hoạt\n⬜ Trả lời 'Không' để từ chối"
        )
        return

    if message_text == "có":
        mark_registered(sender_id)
        send_message(sender_id,
            "✅ Bạn đã đồng ý nhận tín hiệu từ bot Cofure! Bắt đầu từ bản tin sáng lúc 06:00 ⏰"
        )
        return

    if message_text == "không":
        send_message(sender_id,
            "☁️ Bạn đã từ chối nhận tín hiệu. Nếu muốn bắt đầu lại, hãy nhắn 'Có'."
        )
        return
