import requests
import os

# 📌 Token Messenger lấy từ Page Access Token trên Meta Developer
PAGE_TOKEN = os.getenv("MESSENGER_TOKEN")  # Đặt trong file .env

def send_message(user_id, text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }
    params = {
        "access_token": PAGE_TOKEN
    }

    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code != 200:
        print(f"[send_message] ❌ Error: {response.status_code} → {response.text}")
    else:
        print(f"[send_message] ✅ Sent to {user_id}: {text}")
