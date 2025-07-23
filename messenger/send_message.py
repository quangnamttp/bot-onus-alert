# cofure_bot/messenger/send_message.py

import requests
from utils.config_loader import PAGE_ACCESS_TOKEN

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v15.0/me/messages"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Lỗi khi gửi tin nhắn: {e}")
