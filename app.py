from flask import Flask, request
import os
from dotenv import load_dotenv
from messenger import send_message
from market_data import (
    get_kline,
    get_rsi,
    get_price,
    get_volume,
    get_all_symbols
)
from subscribers import add_subscriber
from utils import format_signal
from signal_engine import scan_entry

# 🔧 Tải biến môi trường
load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

# 🚀 Khởi tạo Flask app
app = Flask(__name__)

# ✅ Xác thực Facebook webhook (GET)
@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    return challenge if token == VERIFY_TOKEN else "Invalid token", 403

# ✅ Nhận tin nhắn từ người dùng (POST)
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):
            sender_id = msg["sender"]["id"]
            add_subscriber(sender_id)

            if "message" in msg and "text" in msg["message"]:
                user_text = msg["message"]["text"]
                symbol = extract_symbol(user_text)
                if symbol:
                    response = analyze_symbol(symbol)
                else:
                    response = f"🤖 Không tìm thấy tên coin trong: \"{user_text}\"\nGõ PEPE, OP, DOGE, LDO, v.v. để nhận phân tích kỹ thuật."
                send_message(sender_id, response)

    return "ok", 200

# 🧠 Tự động nhận diện mã giao dịch từ nội dung tin nhắn
def extract_symbol(text):
    text = text.upper().replace("USDT", "")
    user_words = text.split()
    all_symbols = get_all_symbols()

    for word in user_words:
        matches = [s for s in all_symbols if s.startswith(word)]
        if matches:
            return matches[0]  # VD: "PEPE" → "PEPEUSDT"
    return None

# 📊 Phân tích kỹ thuật token
def analyze_symbol(symbol):
    try:
        candles = get_kline(symbol)
        if not candles or len(candles) < 20:
            return f"🚫 Không đủ dữ liệu để phân tích {symbol}"

        rsi = get_rsi(candles)
        price = get_price(symbol)
        volume = get_volume(symbol)
        ma20 = sum([float(k[4]) for k in candles[-20:]]) / 20

        # 🔥 Cảnh báo volume
        avg_vol = sum([float(k[5]) for k in candles[-5:]]) / 5
        volume_warn = volume > avg_vol * 5

        type_ = "LONG" if rsi < 30 and price > ma20 else "SHORT" if rsi > 70 and price < ma20 else "NEUTRAL"

        if type_ == "NEUTRAL":
            return f"🤔 {symbol}: Chưa rõ xu hướng. RSI: {rsi:.2f} | Giá: ${price:.6f}"

        tp = price * (1.05 if type_ == "LONG" else 0.95)
        sl = price * (0.95 if type_ == "LONG" else 1.05)

        signal = {
            "type": type_,
            "symbol": symbol,
            "price": price,
            "rsi": rsi,
            "ma20": ma20,
            "volume": volume,
            "tp": tp,
            "sl": sl,
            "entry_type": "market",
            "volume_warn": volume_warn
        }

        return format_signal(signal)

    except Exception as e:
        return f"🚫 Lỗi khi phân tích {symbol}: {e}"
