import requests
import json
from config import PAGE_ACCESS_TOKEN

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": { "id": recipient_id },
        "message": { "text": text }
    }
    headers = { "Content-Type": "application/json" }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("📨 Gửi tin nhắn:", response.status_code, response.text)
