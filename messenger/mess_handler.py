from messenger.message_sender import send_message
from messenger.registry_manager import (
    is_registered, mark_registered,
    remove_from_registry
)
from utils.mid_tracker import has_processed, mark_processed

def handle_message(event):
    sender_id = event['sender']['id']
    message_text = event['message'].get('text', '').strip().lower()
    mid = event['message'].get('mid', '')

    if has_processed(mid):
        return
    mark_processed(mid)

    # ✅ Nếu đã kích hoạt rồi → không hỏi lại
    if is_registered(sender_id):
        send_message(sender_id, "✅ Bot Cofure đang hoạt động! Tín hiệu sẽ gửi tự động theo từng khung giờ 🚀")
        return

    # 🛑 Nếu người dùng nhắn huỷ bot → xóa khỏi danh sách nhận tín hiệu
    if message_text in ["huỷ bot", "tắt bot", "stop", "cancel"]:
        remove_from_registry(sender_id)
        send_message(sender_id, "❌ Bạn đã tắt bot Cofure. Nếu muốn bật lại, hãy nhắn 'Có'.")
        return

    # 🧠 Hỏi xác nhận nếu chưa đăng ký
    if message_text in ["", "hi", "hello", "chào", "bắt đầu", "start"] or len(message_text) < 5:
        send_message(sender_id,
            "👋 Chào bạn! Đây là bot Cofure gửi tín hiệu crypto tự động.\n🧠 Bạn có muốn nhận tín hiệu không?\n🟩 Trả lời 'Có' để kích hoạt\n⬜ Trả lời 'Không' để từ chối"
        )
        return

    # ✅ Người dùng đồng ý
    if message_text == "có":
        mark_registered(sender_id)
        send_message(sender_id,
            "✅ Bạn đã đồng ý nhận tín hiệu từ bot Cofure! Bắt đầu từ bản tin sáng lúc 06:00 ⏰"
        )
        return

    # 🚫 Người dùng từ chối
    if message_text == "không":
        send_message(sender_id,
            "☁️ Bạn đã từ chối nhận tín hiệu. Nếu muốn bắt đầu lại, hãy nhắn 'Có'."
        )
        return
