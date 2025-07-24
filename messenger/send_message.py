# cofure_bot/messenger/send_message.py

import requests
import logging
from utils.config_loader import PAGE_ACCESS_TOKEN

DEFAULT_TIMEOUT = 5  # seconds
MAX_RETRIES = 2

def _post(payload):
    """
    Internal helper: gửi HTTP request với retry + timeout
    """
    url    = "https://graph.facebook.com/v15.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                url,
                params=params,
                json=payload,
                timeout=DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
            data = resp.json()
            logging.info("✅ Sent OK: %s", data)
            return data
        except Exception as e:
            logging.warning("⚠️ Attempt %d/%d failed: %s", attempt, MAX_RETRIES, e)
            if attempt == MAX_RETRIES:
                logging.exception("❌ All retries failed when sending message")
                return None

def send_message(recipient_id, message_text, messaging_type="RESPONSE", persona_id=None):
    """
    Gửi text thuần túy.
      • messaging_type: RESPONSE | UPDATE | MESSAGE_TAG
      • persona_id: dùng khi bạn có nhiều persona Facebook
    """
    payload = {
        "messaging_type": messaging_type,
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    if persona_id:
        payload["persona_id"] = persona_id

    logging.debug("✉️ send_message payload: %s", payload)
    return _post(payload)

def send_template_message(
    recipient_id,
    text=None,
    template_payload=None,
    quick_replies=None,
    messaging_type="RESPONSE",
    persona_id=None
):
    """
    Gửi template (button/generic) kèm optional text & quick replies.
    • template_payload: dict template_type + elements/buttons
    • quick_replies: list of quick reply dicts
    """
    message = {}
    if text:
        message["text"] = text

    message["attachment"] = {
        "type": "template",
        "payload": template_payload or {}
    }

    if quick_replies:
        message["quick_replies"] = quick_replies

    payload = {
        "messaging_type": messaging_type,
        "recipient": {"id": recipient_id},
        "message": message
    }
    if persona_id:
        payload["persona_id"] = persona_id

    logging.debug("✉️ send_template_message payload: %s", payload)
    return _post(payload)

def send_button_template(recipient_id, text, buttons, quick_replies=None, **kwargs):
    """
    Shortcut: gửi Button Template.
      • buttons: list of {type, title, payload or url}
    """
    payload = {
        "template_type": "button",
        "text": text,
        "buttons": buttons
    }
    return send_template_message(
        recipient_id=recipient_id,
        template_payload=payload,
        quick_replies=quick_replies,
        **kwargs
    )
