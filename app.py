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

load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    return challenge if token == VERIFY_TOKEN else "Invalid token", 403

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
                    response = (
                        f"🤖 Không tìm thấy token trong: \"{user_text}\"\n"
                        f"Gõ PEPE, DOGE, OP, LDO… để nhận phân tích kỹ thuật."
                    )
                send_message(sender_id, response)
    return "ok", 200

def extract_symbol(text):
    text = text.upper().replace("USDT", "")
    words = text.split()
    try:
        all_symbols = get_all_symbols()
        for word in words:
            matches = [s for s in all_symbols if s.startswith(word)]
            if matches:
                print(f"🔍 Khớp: {word} → {matches[0]}")
                return matches[0]
        print(f"❌ Không khớp token nào từ: {text}")
        return None
    except Exception as e:
        print(f"⛔ Lỗi extract_symbol: {e}")
        return None

def analyze_symbol(symbol):
    try:
        candles = get_kline(symbol)
        if not candles or len(candles) < 20:
            return f"🚫 Không đủ dữ liệu để phân tích {symbol}"

        rsi = get_rsi(candles)
        price = get_price(symbol)
        volume = get_volume(symbol)
        ma20 = sum([float(k[4]) for k in candles[-20:]]) / 20

        avg_vol = sum([float(k[5]) for k in candles[-5:]]) / 5
        volume_warn = volume > avg_vol * 5
        if volume_warn:
            print(f"⚠️ Volume tăng mạnh ở {symbol}: {volume:.2f}")

        type_ = (
            "LONG" if rsi < 30 and price > ma20 else
            "SHORT" if rsi > 70 and price < ma20 else
            "NEUTRAL"
        )

        if type_ == "NEUTRAL":
            return f"🤔 {symbol}: Chưa có xu hướng rõ ràng. RSI: {rsi:.2f} | Giá: ${price:.6f}"

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
        print(f"⛔ Lỗi phân tích {symbol}: {e}")
        return f"🚫 Lỗi khi xử lý token {symbol}"
