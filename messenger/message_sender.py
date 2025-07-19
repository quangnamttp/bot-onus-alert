import os
import requests

ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

def send_message(psid, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": psid},
        "message": {"text": message_text}
    }
    requests.post(url, headers=headers, json=payload)
