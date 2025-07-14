import requests
import os
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

def send_message(recipient_id, message_text):
    """
    Gửi tin nhắn văn bản đến người dùng qua Facebook Messenger.
    """
    url = "https://graph.facebook.com/v17.0/me/messages"
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": { "id": recipient_id },
        "message": { "text": message_text }
    }

    try:
        res = requests.post(url, params=params, headers=headers, json=data)
        res.raise_for_status()
        print(f"✅ Tin nhắn đã gửi: {message_text}")
    except Exception as e:
        print(f"⛔ Lỗi khi gửi tin nhắn Messenger: {e}")
