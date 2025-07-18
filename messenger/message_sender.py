import os
import requests

FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")

def send_message(recipient_id, message_text):
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={FB_PAGE_TOKEN}"
    headers = {"Content-Type": "application/json"}
    requests.post(url, headers=headers, json=payload)
