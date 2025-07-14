from flask import Flask, request
import os
from dotenv import load_dotenv
from messenger import send_message
from market_data import get_kline, get_rsi, get_price, get_volume, check_symbol_exists
from subscribers import add_subscriber
from utils import format_signal
from signal_engine import scan_entry

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
                user_text = msg["message"]["text"].lower()
                symbol = extract_symbol(user_text)
                if symbol:
                    response = analyze_symbol(symbol)
                else:
                    response = "📌 Bot ONUS sẵn sàng! Gõ tên coin (VD: PEPE, DOGE, OP) để nhận phân tích."
                send_message(sender_id, response)

    return "ok", 200

def extract_symbol(text):
    text = text.upper().replace("USDT", "")
    words = text.split()
    for word in words:
        symbol = word + "USDT"
        if check_symbol_exists(symbol):
            return symbol
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

        type_ = "LONG" if rsi < 30 and price > ma20 else "SHORT" if rsi > 70 and price < ma20 else "NEUTRAL"

        if type_ == "NEUTRAL":
            return f"🤔 {symbol}: Chưa rõ xu hướng mạnh. RSI: {rsi:.2f} | Giá: ${price:.6f}"

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
            "entry_type": "market"
        }
        return format_signal(signal)

    except Exception as e:
        return f"🚫 Lỗi khi phân tích {symbol}: {e}"
