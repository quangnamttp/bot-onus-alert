import requests
import os
from dotenv import load_dotenv

load_dotenv()
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    try:
        res = requests.post(url, params=params, headers=headers, json=data)
        res.raise_for_status()
        print(f"✅ Tin nhắn đã gửi: {message_text}")
    except Exception as e:
        print(f"⛔ Lỗi gửi tin nhắn: {e}")
