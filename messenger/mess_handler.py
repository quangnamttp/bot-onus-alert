from messenger.message_sender import send_message
from messenger.registry_manager import is_registered, is_pending, mark_pending
from utils.mid_tracker import has_processed, mark_processed

def handle_message(event):
    sender_id = event['sender']['id']
    message_text = event['message'].get('text', '').strip().lower()
    mid = event['message'].get('mid', '')

    # 🔁 Chống phản hồi trùng nếu Facebook gửi lại payload
    if has_processed(mid):
        return
    mark_processed(mid)

    # ✅ Nếu người dùng đã được duyệt → bot hoạt động bình thường
    if is_registered(sender_id):
        # Tại đây gắn xử lý gửi tín hiệu, nhận lệnh, broadcast v.v.
        return

    # ⌛ Nếu người dùng đã chọn "Có" và đang chờ duyệt → không phản hồi nữa
    if is_pending(sender_id):
        return

    # 🧠 Nếu người dùng nhắn tin lần đầu tiên → bot hỏi xác nhận
    if message_text in ["", "hi", "hello", "chào", "bắt đầu", "start"]:
        send_message(sender_id,
            "📩 Chào bạn! Bot Cofure chuyên gửi tín hiệu trade kỹ thuật theo sàn ONUS mỗi ngày từ 06:00 đến 22:00\n📈 Bạn có muốn nhận tín hiệu lệnh hôm nay không?\n🟩 Trả lời “Có” để bắt đầu quy trình duyệt\n⬜ Trả lời “Không” nếu bạn không muốn sử dụng bot"
        )
        return

    # ✅ Nếu người dùng trả lời "Có" → bot ghi vào pending_users.json + gửi link duyệt
    if message_text == "có":
        mark_pending(sender_id)
        send_message(sender_id,
            "📥 Cofure đã ghi nhận yêu cầu nhận lệnh của bạn\n📩 Vui lòng liên hệ admin [Trương Tấn Phương](https://www.facebook.com/quangnamttp) để được phê duyệt\n✅ Sau khi được duyệt, bot sẽ bắt đầu gửi tín hiệu trade mỗi ngày theo sàn ONUS!"
        )
        return

    # ❌ Nếu người dùng trả lời "Không" → bot im lặng, không phản hồi
    if message_text == "không":
        return

    # 📬 Nếu user gửi nội dung khác → bot giữ im lặng để tránh spam
    return
