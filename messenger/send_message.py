# cofure_bot/messenger/send_message.py
import requests, logging
from utils.config_loader import PAGE_ACCESS_TOKEN

def send_message(recipient_id, message_text):
    """
    Gửi text thuần túy
    """
    url = "https://graph.facebook.com/v15.0/me/messages"
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}

    try:
        resp = requests.post(url, params=params, json=payload)
        resp.raise_for_status()
        logging.info(f"✅ Sent text message to {recipient_id}")
    except Exception as e:
        logging.exception(f"❌ Lỗi khi gửi tin nhắn: {e}")

def send_template_message(recipient_id, text, template_payload, quick_replies=None):
    """
    Gửi attachment template (button/generic) kèm quick replies
    """
    url = "https://graph.facebook.com/v15.0/me/messages"
    message = {
        "attachment": {
            "type": "template",
            "payload": template_payload
        }
    }
    if quick_replies:
        message["quick_replies"] = quick_replies

    payload = {
        "recipient": {"id": recipient_id},
        "message": message
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}

    try:
        resp = requests.post(url, params=params, json=payload)
        resp.raise_for_status()
        logging.info(f"✅ Sent template message to {recipient_id}")
    except Exception as e:
        logging.exception(f"❌ Lỗi khi gửi template message: {e}")
