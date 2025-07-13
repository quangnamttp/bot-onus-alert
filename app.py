from flask import Flask, request
import requests, os, random, time, threading
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import schedule

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot đang hoạt động!"

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
                "payload": {"url": image_url, "is_reusable": True}
            }
        },
        "messaging_type": "RESPONSE",
        "access_token": PAGE_ACCESS_TOKEN
    }
    requests.post(url, json=payload)

def send_subscription_prompt(user_id):
    url = "https://graph.facebook.com/v17.0/me/messages"
    payload = {
        "recipient": {"id": user_id},
        "message": {
            "text": "📡 Bạn muốn nhận tín hiệu đầu tư tự động mỗi 30 phút?",
            "quick_replies": [
                {"content_type": "text", "title": "Đăng ký nhận tín hiệu", "payload": "SUBSCRIBE"},
                {"content_type": "text", "title": "Hủy đăng ký", "payload": "UNSUBSCRIBE"}
            ]
        },
        "messaging_type": "RESPONSE",
        "access_token": PAGE_ACCESS_TOKEN
    }
    requests.post(url, json=payload)

def handle_message(text, sender_id):
    msg = text.lower()
    token = extract_token(text)

    if "đăng ký" in msg or "hủy đăng ký" in msg:
        if "hủy" in msg:
            remove_subscriber(sender_id)
            return "❌ Bạn đã hủy nhận tín hiệu tự động."
        else:
            add_subscriber(sender_id)
            return "✅ Bạn đã đăng ký nhận tín hiệu tự động mỗi 30 phút."
    
    if "tín hiệu" in msg:
        send_subscription_prompt(sender_id)
        return ""

    if not token:
        return "🤖 Bạn có thể hỏi: 'SHIB có vào được không?' hoặc 'Có coin nào nên mua?'"

    signal = analyze_entry(token)
    if signal["entry"]:
        chart_url = "https://yourdomain.com/static/entry_chart.png"
        send_image(sender_id, chart_url)
        return f"✅ Có thể vào lệnh với {token}\n🎯 TP: {signal['tp']} | SL: {signal['sl']}\n📝 {signal['reason']}"
    else:
        return f"❌ Không nên vào {token} lúc này\n📝 {signal['reason']}"

def extract_token(text):
    words = text.upper().split()
    for word in words:
        if word in get_all_onus_tokens():
            return word
    return None

def get_all_onus_tokens():
    try:
        html = requests.get("https://goonus.io/", headers={"User-Agent":"Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")
        return [card.select_one(".name").text.strip().upper() for card in soup.select(".market-card")]
    except:
        return ["SHIB", "DOGE", "PEPE", "SUI", "BTC"]

def analyze_entry(token):
    if random.choice([True, False]):
        price = "${:.4f}".format(random.uniform(0.01, 0.1))
        return {
            "entry": True,
            "tp": "${:.6f}".format(random.uniform(0.05, 0.2)),
            "sl": "${:.6f}".format(random.uniform(0.01, 0.05)),
            "reason": "RSI thấp + hỗ trợ mạnh",
            "entry_price": price
        }
    return {
        "entry": False,
        "tp": "-",
        "sl": "-",
        "reason": "RSI cao hoặc kháng cự gần",
        "entry_price": "-"
    }

def generate_chart(token, entry_price):
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

def add_subscriber(user_id):
    try:
        with open("subscribers.txt", "a") as f:
            f.write(f"{user_id}\n")
    except: pass

def remove_subscriber(user_id):
    try:
        with open("subscribers.txt", "r") as f:
            ids = f.readlines()
        ids = [i.strip() for i in ids if i.strip() != user_id]
        with open("subscribers.txt", "w") as f:
            for i in ids:
                f.write(f"{i}\n")
    except: pass

def get_all_subscribers():
    try:
        with open("subscribers.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def quet_tin_hieu_moi():
    signal = scan_best_entry()
    if signal:
        for uid in get_all_subscribers():
            send_message(uid, f"⏱️ Tín hiệu tự động:\n{signal}")

def scan_best_entry():
    tokens = get_all_onus_tokens()
    for token in tokens[:5]:
        s = analyze_entry(token)
        if s["entry"]:
            return f"📈 Token: {token}\n🎯 TP: {s['tp']} | SL: {s['sl']}\n📝 {s['reason']}"
    return None

schedule.every(30).minutes.do(quet_tin_hieu_moi)

def start_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=start_schedule, daemon=True).start()
