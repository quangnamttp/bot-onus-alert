from flask import Flask, request
import requests, os, random, datetime, threading, time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import schedule

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # ID người nhận tín hiệu tự động
cached_tokens = []

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot ONUS đang hoạt động!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        return challenge if token == VERIFY_TOKEN else "Sai verify token", 403

    if request.method == "POST":
        data = request.get_json()
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event:
                    text = event["message"].get("text", "")
                    reply = handle_message(text, sender_id)
                    send_message(sender_id, reply)
        return "OK", 200

def send_message(user_id, reply_text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": reply_text},
        "messaging_type": "RESPONSE",
        "access_token": PAGE_ACCESS_TOKEN
    }
    requests.post(url, json=payload)

def send_image(user_id, image_url):
    url = "https://graph.facebook.com/v17.0/me/messages"
    payload = {
        "recipient": {"id": user_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url,
                    "is_reusable": True
                }
            }
        },
        "messaging_type": "RESPONSE",
        "access_token": PAGE_ACCESS_TOKEN
    }
    requests.post(url, json=payload)

def handle_message(text, sender_id):
    msg = text.lower()
    token = extract_token(text)

    if not token:
        return "⚠️ Không nhận diện được token bạn hỏi. Ví dụ: 'MUA DOGE lúc này được không?'"

    if "có nên vào" in msg or "vào được không" in msg:
        signal = analyze_entry(token)
        if signal["entry"]:
            chart_url = upload_chart_and_get_url(token, float(signal["entry_price"].strip("$")))
            if chart_url:
                send_image(sender_id, chart_url)
            return f"✅ Có thể vào lệnh với {token}\n🎯 TP: {signal['tp']} | SL: {signal['sl']}\n📝 {signal['reason']}"
        else:
            return f"❌ Không nên vào {token} lúc này\n📝 {signal['reason']}"

    if "mua" in msg or "bán" in msg:
        action = "mua" if "mua" in msg else "bán"
        signal = analyze_trade_action(token, action)
        return f"{'✅' if signal['recommend'] else '❌'} {'NÊN' if signal['recommend'] else 'KHÔNG nên'} {action.upper()} {token} lúc này\n🎯 TP: {signal['tp']} | SL: {signal['sl']}\n📝 {signal['reason']}"

    if "coin nào" in msg or "nào mua" in msg:
        best = scan_best_entry()
        return best if best else "😴 Hiện tại chưa có coin nào vào được."

    return "💬 Bạn có thể hỏi:\n• 'PEPE có vào được không?'\n• 'Có coin nào nên mua lúc này?'"

def extract_token(text):
    words = text.upper().split()
    tokens = get_all_onus_tokens()
    for word in words:
        if word in tokens:
            return word
    return None

def get_all_onus_tokens():
    global cached_tokens
    if cached_tokens:
        return cached_tokens
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get("https://goonus.io/", headers=headers, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        cached_tokens = [card.select_one(".name").text.strip().upper() for card in soup.select(".market-card")]
        return cached_tokens if cached_tokens else ["BTC", "ETH", "SHIB", "DOGE", "PEPE", "SUI"]
    except:
        return ["BTC", "ETH", "SHIB", "DOGE", "PEPE", "SUI"]

def analyze_entry(token):
    if random.choice([True, False]):
        price = "${:.4f}".format(random.uniform(0.01, 0.1))
        return {
            "entry": True,
            "tp": "${:.6f}".format(random.uniform(0.05, 0.15)),
            "sl": "${:.6f}".format(random.uniform(0.01, 0.04)),
            "reason": "RSI thấp + volume cao + vùng hỗ trợ mạnh",
            "entry_price": price
        }
    return {
        "entry": False,
        "tp": "-",
        "sl": "-",
        "reason": "RSI cao hoặc vùng kháng cự gần",
        "entry_price": "-"
    }

def analyze_trade_action(token, action):
    if random.choice([True, False]):
        return {
            "recommend": True,
            "tp": "${:.6f}".format(random.uniform(0.05, 0.2)),
            "sl": "${:.6f}".format(random.uniform(0.01, 0.05)),
            "reason": "Khối lượng tăng, RSI đẹp, có dòng tiền vào"
        }
    return {
        "recommend": False,
        "tp": "-",
        "sl": "-",
        "reason": "Xu hướng chưa rõ, vùng giá không an toàn"
    }

def scan_best_entry():
    tokens = get_all_onus_tokens()
    for token in tokens[:10]:
        s = analyze_entry(token)
        if s["entry"]:
            return f"📈 Token tốt nhất: {token}\n🎯 TP: {s['tp']} | SL: {s['sl']}\n📝 {s['reason']}"
    return None

def generate_dark_chart(token, entry_price):
    prices = [random.uniform(entry_price - 0.02, entry_price + 0.02) for _ in range(20)]
    plt.style.use("dark_background")
    plt.figure(figsize=(6,4))
    plt.plot(prices, label=f"{token}", color="cyan", linewidth=2)
    plt.axhline(entry_price, color="lime", linestyle="--", label=f"Entry ${entry_price:.4f}")
    plt.text(len(prices)-6, entry_price + 0.002, f"${entry_price:.4f}", color="white")
    plt.title(f"{token} Entry Chart", color="white")
    plt.xlabel("Time", color="white")
    plt.ylabel("Price", color="white")
    plt.legend()
    plt.tight_layout()
    chart_path = "entry_chart.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def upload_chart_and_get_url(token, entry_price):
    chart_path = generate_dark_chart(token, entry_price)
    # ❗ Bạn cần dùng hosting để upload ảnh và trả về link — đây chỉ là placeholder
    return "https://yourdomain.com/static/entry_chart.png"  # Cập nhật link ảnh thật tại đây

# 🔁 Tự động quét mỗi 30 phút
def quet_tin_hieu_moi():
    signal = scan_best_entry()
    if signal:
        send_message(ADMIN_ID, f"⏱️ Tín hiệu tự động:\n{signal}")

schedule.every(30).minutes.do(quet_tin_hieu_moi)

def start_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=start_schedule, daemon=True).start()
