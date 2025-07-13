from flask import Flask, request
import requests, os, random, datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot giao dịch crypto đang hoạt động!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Sai verify token", 403

    if request.method == "POST":
        data = request.get_json()
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event:
                    text = event["message"].get("text", "")
                    reply = process_message(text)
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

def process_message(text):
    msg = text.lower()
    token = extract_token(text)

    if "vào được không" in msg or "có nên vào" in msg:
        signal = analyze_entry(token)
        if signal["entry"]:
            return f"✅ Có thể vào {token}\n🎯 TP: {signal['tp']} | SL: {signal['sl']}\n📝 Lý do: {signal['reason']}"
        else:
            return f"❌ Không nên vào {token} lúc này\n📝 {signal['reason']}"

    elif "entry đẹp" in msg:
        return auto_entry_scan()

    elif "cảnh báo" in msg or "cá voi" in msg or "whale" in msg:
        return whale_alerts()

    elif "pump" in msg or "tăng" in msg or "giá" in msg:
        data = fetch_onus_tokens()
        return "📊 Token đang pump:\n" + "\n".join(data)

    return "💬 Bạn có thể hỏi:\n• 'DOGE có vào được không'\n• 'Cảnh báo cá voi'\n• 'Entry đẹp'\n• 'Token đang pump'"

def extract_token(text):
    words = text.upper().split()
    known = ["PEPE", "DOGE", "SHIB", "SUI", "APT", "BTC", "ETH", "VNDC", "ONUS"]
    for w in words:
        if w in known:
            return w
    return "?"

def analyze_entry(token):
    # Phân tích giả lập
    entry = random.choice([True, False])
    if entry:
        return {
            "entry": True,
            "tp": "$" + str(round(random.uniform(0.0004, 0.1), 6)),
            "sl": "$" + str(round(random.uniform(0.0003, 0.08), 6)),
            "reason": "RSI thấp + volume tăng + giá gần vùng hỗ trợ"
        }
    return {
        "entry": False,
        "tp": "-",
        "sl": "-",
        "reason": "RSI cao, kháng cự mạnh, dòng tiền yếu"
    }

def auto_entry_scan():
    tokens = ["PEPE", "DOGE", "SHIB", "SUI", "APT"]
    entries = []
    for t in tokens:
        s = analyze_entry(t)
        if s["entry"]:
            entries.append(f"✅ {t}: TP {s['tp']} | SL {s['sl']} — {s['reason']}")
    return "📈 Entry đẹp hiện tại:\n" + ("\n".join(entries) if entries else "😴 Không có entry đẹp lúc này")

def whale_alerts():
    now = datetime.datetime.now().strftime("%H:%M")
    alerts = [
        f"🟢 {now} – Cá voi vừa mua 100B SHIB",
        f"🔴 {now} – Cá voi xả 500M DOGE",
        f"🟡 {now} – Dòng tiền lớn vào SUI từ ví cá nhân"
    ]
    return "📡 Cảnh báo dòng tiền:\n" + "\n".join(alerts)

def fetch_onus_tokens():
    try:
        html = requests.get("https://goonus.io/").text
        soup = BeautifulSoup(html, "html.parser")
        tokens = []
        for card in soup.select(".market-card")[:3]:
            name = card.select_one(".name").text.strip()
            price = card.select_one(".price").text.strip()
            percent = card.select_one(".percent").text.strip()
            tokens.append(f"🔥 {name}: {price} ({percent})")
        return tokens
    except:
        return ["⚠️ Không lấy được dữ liệu ONUS"]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

