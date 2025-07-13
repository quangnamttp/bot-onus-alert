import time
from signal_engine import scan_entry
import requests
import os

# ==== DỮ LIỆU FACEBOOK ====
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

# ==== ĐỌC DANH SÁCH SUBSCRIBERS ====
def get_subscribers():
    try:
        with open("subscribers.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except:
        return []

# ==== GỬI TIN NHẮN FACEBOOK ====
def send_message(recipient_id, message):
    url = 'https://graph.facebook.com/v18.0/me/messages'
    headers = { "Content-Type": "application/json" }
    payload = {
        "recipient": { "id": recipient_id },
        "message": { "text": message },
        "messaging_type": "UPDATE",
        "access_token": PAGE_ACCESS_TOKEN
    }
    requests.post(url, headers=headers, json=payload)

# ==== CHẠY VÒNG LẶP GỬI TÍN HIỆU ====
def auto_loop():
    while True:
        print("🔄 Đang quét tín hiệu vào lệnh...")
        signal = scan_entry()
        if signal:
            msg = (
                f"📢 Tín hiệu mới {signal['symbol']}:\n"
                f"- Giá vào lệnh: ${signal['entry']}\n"
                f"- RSI: {signal['rsi']}\n"
                f"- MA20: {signal['ma']}\n"
                f"- Volume: {signal['volume']:,}\n"
                f"👉 Có thể cân nhắc vào lệnh nếu phù hợp chiến lược!"
            )
            for uid in get_subscribers():
                send_message(uid, msg)
            print(f"✅ Đã gửi tín hiệu {signal['symbol']} cho {len(get_subscribers())} người đăng ký.")
        else:
            print("⛔ Không có tín hiệu phù hợp lúc này.")
        time.sleep(300)  # Chờ 5 phút rồi quét lại
