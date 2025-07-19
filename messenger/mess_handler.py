from messenger.message_sender import send_message
from messenger.registry_manager import is_registered, is_pending, mark_pending
from utils.mid_tracker import has_processed, mark_processed
from admin.config_loader import get_admin_psid
from datetime import datetime

def handle_message(event):
    sender_id = event['sender']['id']
    message_text = event['message'].get('text', '').strip().lower()
    mid = event['message'].get('mid', '')

    # 🔁 Chống phản hồi trùng nếu Facebook gửi lại payload
    if has_processed(mid):
        return
    mark_processed(mid)

    # ✅ Nếu user đã được duyệt → bot hoạt động bình thường (gửi tín hiệu, bản tin…)
    if is_registered(sender_id):
        # Có thể gọi các hàm sinh tín hiệu, gửi bản tin… tại đây
        return

    # ⌛ Nếu user đang chờ duyệt → không phản hồi thêm
    if is_pending(sender_id):
        return

    # 🧠 Nếu người dùng nhắn lần đầu hoặc gửi nội dung không rõ ràng → hỏi xác nhận
    if message_text in ["", "hi", "hello", "chào", "bắt đầu", "start"] or len(message_text) < 5:
        send_message(sender_id,
            "📩 Chào bạn! Bot Cofure chuyên gửi tín hiệu trade kỹ thuật theo sàn ONUS mỗi ngày từ 06:00 đến 22:00\n📈 Bạn có muốn nhận tín hiệu lệnh hôm nay không?\n🟩 Trả lời “Có” để bắt đầu quy trình duyệt\n⬜ Trả lời “Không” nếu bạn không muốn sử dụng bot"
        )
        return

    # ✅ Nếu user trả lời "Có" → ghi vào pending + gửi tin hướng dẫn + báo về admin
    if message_text == "có":
        mark_pending(sender_id)

        # Gửi hướng dẫn cho người dùng
        send_message(sender_id,
            "📥 Cofure đã ghi nhận yêu cầu nhận lệnh của bạn\n📩 Vui lòng liên hệ admin [Trương Tấn Phương](https://www.facebook.com/quangnamttp) để được phê duyệt\n✅ Sau khi được duyệt, bot sẽ bắt đầu gửi tín hiệu trade mỗi ngày theo sàn ONUS!"
        )

        # Gửi cảnh báo về bạn (admin) để xét duyệt
        admin_id = get_admin_psid()
        send_message(admin_id,
            f"📬 Người dùng vừa yêu cầu nhận tín hiệu từ Cofure\n👤 PSID: {sender_id}\n🕒 Thời điểm: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n📋 Duyệt bằng lệnh: /duyet {sender_id}"
        )
        return

    # ❌ Nếu user trả lời "Không" → bot không phản hồi
    if message_text == "không":
        return

    # 🧱 Nếu nội dung không khớp gì → giữ im lặng để tránh spam
    return
