from messenger.message_sender import send_message
from messenger.registry_manager import is_registered, is_pending, mark_pending
from utils.mid_tracker import has_processed, mark_processed
from admin.config_loader import get_admin_psid
from datetime import datetime

def handle_message(event):
    sender_id = event['sender']['id']
    message_text = event['message'].get('text', '').strip().lower()
    mid = event['message'].get('mid', '')

    # 🔁 Chống phản hồi trùng payload từ Messenger
    if has_processed(mid):
        return
    mark_processed(mid)

    # ✅ Người dùng đã được duyệt → bot hoạt động bình thường
    if is_registered(sender_id):
        # Gắn gửi tín hiệu, lệnh Futures hoặc bản tin tại đây
        return

    # ⌛ Người dùng đã xác nhận “Có” nhưng chưa được duyệt
    if is_pending(sender_id):
        return

    # 🧠 Người dùng nhắn lần đầu → bot hỏi có muốn nhận tín hiệu không
    if message_text in ["", "hi", "hello", "chào", "bắt đầu", "start"] or len(message_text) < 5:
        send_message(sender_id,
            "📩 Chào bạn! Bot Cofure chuyên gửi tín hiệu trade kỹ thuật theo sàn ONUS mỗi ngày từ 06:00 đến 22:00\n📈 Bạn có muốn nhận tín hiệu lệnh hôm nay không?\n🟩 Trả lời “Có” để bắt đầu quy trình duyệt\n⬜ Trả lời “Không” nếu bạn không muốn sử dụng bot"
        )
        return

    # ✅ Người dùng trả lời “Có” → ghi PSID + hướng dẫn duyệt + báo admin
    if message_text == "có":
        mark_pending(sender_id)
        send_message(sender_id,
            "📥 Cofure đã ghi nhận yêu cầu nhận lệnh của bạn\n📩 Vui lòng liên hệ admin [Trương Tấn Phương](https://www.facebook.com/quangnamttp) để được phê duyệt\n✅ Sau khi được duyệt, bot sẽ bắt đầu gửi tín hiệu trade mỗi ngày theo sàn ONUS!"
        )
        admin_id = get_admin_psid()
        send_message(admin_id,
            f"📬 Người dùng vừa yêu cầu nhận tín hiệu từ Cofure\n👤 PSID: {sender_id}\n🕒 Thời điểm: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n📋 Duyệt bằng lệnh: /duyet {sender_id}"
        )
        return

    # ❌ Người dùng trả lời “Không” → bot không phản hồi
    if message_text == "không":
        return

    return
