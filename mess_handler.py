import os, requests, json
from exchange_router import get_price

def load_recipients():
    try:
        with open("recipient_list.json") as f:
            return json.load(f)["recipients"]
    except: return []

def send_message(content, platform="Messenger"):
    if platform == "Messenger":
        url = "https://graph.facebook.com/v17.0/me/messages"
        token = os.getenv("FB_PAGE_TOKEN")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        for psid in load_recipients():
            price = get_price(psid)  # Lấy giá theo sàn của người dùng
            message = content.replace("{price}", f"{price:,}")
            payload = {"recipient": {"id": psid}, "message": {"text": message}}
            r = requests.post(url, json=payload, headers=headers)
            print(f"📤 Sent to {psid}: {r.status_code}")
