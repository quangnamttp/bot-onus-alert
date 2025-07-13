import os
import requests
from flask import Flask, request
import re

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "peacelayer1")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

# ==== GỬI TIN NHẮN ====
def send_message(recipient_id, message):
    url = 'https://graph.facebook.com/v18.0/me/messages'
    headers = { "Content-Type": "application/json" }
    payload = {
        "recipient": { "id": recipient_id },
        "message": { "text": message },
        "messaging_type": "RESPONSE",
        "access_token": PAGE_ACCESS_TOKEN
    }
    requests.post(url, headers=headers, json=payload)

# ==== LẤY GIÁ TỪ BINANCE ====
def get_binance_data(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}USDT"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return {
            "price": float(data["lastPrice"]),
            "change": float(data["priceChangePercent"]),
            "volume": float(data["quoteVolume"])
        }
    return None

# ==== WEBHOOK FACEBOOK ====
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        return challenge if token == VERIFY_TOKEN else "Sai token", 403

    elif request.method == 'POST':
        data = request.get_json()
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender = event.get("sender", {}).get("id")
                message = event.get("message", {}).get("text")
                if sender and message:
                    handle_message(sender, message)
        return "OK", 200

# ==== XỬ LÝ TIN NHẮN ====
def handle_message(sender_id, text):
    cleaned = text.strip().lower()
    match = re.search(r'\b([a-zA-Z0-9]{2,10})\b', cleaned)

    if match:
        symbol = match.group(1).upper()
        send_message(sender_id, f"⏳ Đang kiểm tra dữ liệu {symbol}...")
        info = get_binance_data(symbol)
        if info:
            if "giá" in cleaned or "bao nhiêu" in cleaned:
                reply = (
                    f"📊 {symbol} hiện tại:\n"
                    f"- Giá: ${info['price']:,}\n"
                    f"- Biến động 24h: {info['change']:.2f}%\n"
                    f"- Volume: ${info['volume']:,}"
                )
            elif "vào lệnh" in cleaned or "có vào được không" in cleaned:
                # Giả sử entry hợp lý khi biến động > 3% và volume cao
                if info['change'] > 3 and info['volume'] > 10000000:
                    reply = (
                        f"✅ {symbol} đang có tín hiệu mạnh:\n"
                        f"- Giá hiện tại: ${info['price']:,}\n"
                        f"- Biến động 24h: {info['change']:.2f}%\n"
                        f"- Volume: ${info['volume']:,}\n"
                        f"👉 Có thể cân nhắc vào lệnh nếu phù hợp chiến lược!"
                    )
                else:
                    reply = (
                        f"⚠️ {symbol} chưa có tín hiệu rõ ràng:\n"
                        f"- Giá: ${info['price']:,}\n"
                        f"- Biến động 24h: {info['change']:.2f}%\n"
                        f"- Volume: ${info['volume']:,}\n"
                        f"👉 Nên chờ thêm xác nhận hoặc volume mạnh hơn."
                    )
            else:
                reply = (
                    f"📊 {symbol} hiện tại:\n"
                    f"- Giá: ${info['price']:,}\n"
                    f"- Biến động 24h: {info['change']:.2f}%\n"
                    f"- Volume: ${info['volume']:,}"
                )
        else:
            reply = f"❌ Không tìm thấy dữ liệu cho `{symbol}` trên Binance."
    else:
        reply = (
            "🤖 Bạn có thể hỏi:\n"
            "- 'BTC giá bao nhiêu?'\n"
            "- 'SHIB có vào được không?'\n"
            "- 'SOL có nên vào lệnh không?'"
        )

    send_message(sender_id, reply)
