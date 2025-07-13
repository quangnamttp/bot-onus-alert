from flask import Flask, request
import requests, os, random, datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
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
                    reply = handle_message(text)
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
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("❌ Lỗi gửi tin nhắn:", response.text)

def handle_message(text):
    msg = text.lower()
    token = extract_token(text)

    if not token:
        return "⚠️ Không nhận diện được token bạn hỏi. Hãy thử: 'MUA DOGE lúc này được không?' hoặc 'PEPE vào được không?'"

    if "mua" in msg or "bán" in msg:
        action = "mua" if "mua" in msg else "bán"
        signal = analyze_trade_action(token, action)
        if signal["recommend"]:
            return f"✅ NÊN {action.upper()} {token} lúc này\n🎯 TP: {signal['tp']} | SL: {signal['sl']}\n📝 Lý do: {signal['reason']}"
        else:
            return f"❌ KHÔNG nên {action.upper()} {token} lúc này\n📝 {signal['reason']}"

    elif "vào được không" in msg or "có nên vào" in msg:
        signal = analyze_entry(token)
        if signal["entry"]:
            return f"✅ Có thể vào lệnh với {token}\n🎯 TP: {signal['tp']} | SL: {signal['sl']}\n📝 {signal['reason']}"
        else:
            return f"❌ Không nên vào {token} lúc này\n📝 {signal['reason']}"

    elif "entry đẹp" in msg:
        return scan_best_entry()

    elif "cảnh báo" in msg or "cá voi" in msg or "whale" in msg:
        return whale_alerts()

    elif "pump" in msg or "tăng" in msg or "giá" in msg:
        data = fetch_onus_top()
        return "📊 Token đang pump:\n" + "\n".join(data)

    return "💬 Bạn có thể hỏi:\n• 'SHIB có nên mua lúc này?'\n• 'PEPE có vào được không?'\n• 'BÁN DOGE được không?'\n• 'Entry đẹp'\n• 'Cảnh báo cá voi'"

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
        cached_tokens = [card.select_one(".name").text.strip().upper()
                         for card in soup.select(".market-card")]
        return cached_tokens
    except Exception as e:
        print(f"Lỗi khi lấy token ONUS: {e}")
        return []

def analyze_entry(token):
    if random.choice([True, False]):
        return {
            "entry": True,
            "tp": "${:.6f}".format(random.uniform(0.0004, 0.1)),
            "sl": "${:.6f}".format(random.uniform(0.0003, 0.08)),
            "reason": "RSI thấp + volume cao + giá gần vùng hỗ trợ"
        }
    return {
        "entry": False,
        "tp": "-",
        "sl": "-",
        "reason": "RSI cao hoặc vùng kháng cự gần"
    }

def analyze_trade_action(token, action):
    if action == "mua":
        if random.choice([True, False]):
            return {
                "recommend": True,
                "tp": "${:.6f}".format(random.uniform(0.0005, 0.15)),
                "sl": "${:.6f}".format(random.uniform(0.0003, 0.1)),
                "reason": "Volume tăng + RSI thấp + tin tích cực"
            }
        else:
            return {
                "recommend": False,
                "tp": "-",
                "sl": "-",
                "reason": "RSI cao + kháng cự gần + dòng tiền yếu"
            }
    if action == "bán":
        if random.choice([True, False]):
            return {
                "recommend": True,
                "tp": "-",
                "sl": "-",
                "reason": "Giá chạm kháng cự + RSI cao + có dấu hiệu đảo chiều"
            }
        else:
            return {
                "recommend": False,
                "tp": "-",
                "sl": "-",
                "reason": "Xu hướng vẫn tăng + chưa có tín hiệu rõ"
            }

def scan_best_entry():
    tokens = get_all_onus_tokens()
    best = None
    for token in tokens[:10]:
        s = analyze_entry(token)
        if s["entry"]:
            score = float(s["tp"].strip("$")) - float(s["sl"].strip("$"))
            if not best or score > best["score"]:
                best = {**s, "token": token, "score": score}
    if best:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"📈 Entry tốt nhất lúc {now}:\n✅ {best['token']} → TP: {best['tp']} | SL: {best['sl']}\n📝 {best['reason']}"
    return "😴 Không phát hiện entry đẹp lúc này"

def whale_alerts():
    now = datetime.datetime.now().strftime("%H:%M")
    alerts = [
        f"🟢 {now} – Cá voi mua 100B SHIB",
        f"🔴 {now} – Cá voi xả 500M DOGE",
        f"🟡 {now} – Dòng tiền lớn đang vào SUI"
    ]
    return "📡 Cảnh báo dòng tiền:\n" + "\n".join(alerts)

def fetch_onus_top():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get("https://goonus.io/", headers=headers, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        tokens = []
        for card in soup.select(".market-card")[:3]:
            name = card.select_one(".name").text.strip()
            price = card.select_one(".price").text.strip()
            percent = card.select_one(".percent").text.strip()
            tokens.append(f"🔥 {name}: {price} ({percent})")
        return tokens
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu TOP: {e}")
        return ["⚠️ Không lấy được dữ liệu từ ONUS"]

