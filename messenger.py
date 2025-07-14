# messenger.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
SEND_API_URL = "https://graph.facebook.com/v17.0/me/messages"

def send_message(user_id, text):
    """Gửi tin nhắn văn bản tới người dùng"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE",
    }
    requests.post(SEND_API_URL, params={"access_token": ACCESS_TOKEN}, json=payload, headers=headers)

def send_image(user_id, image_url):
    """Gửi ảnh biểu đồ kỹ thuật tới người dùng"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": user_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url,
                    "is_reusable": True
                }
            }
        }
    }
    requests.post(SEND_API_URL, params={"access_token": ACCESS_TOKEN}, json=payload, headers=headers)

def send_signal_to_all(user_id, message, image_url=None):
    """Gửi tín hiệu kèm ảnh (nếu có) tới người dùng"""
    send_message(user_id, message)
    if image_url:
        send_image(user_id, image_url)
