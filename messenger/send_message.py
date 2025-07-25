import requests
import logging
import json
from utils.config_loader import PAGE_ACCESS_TOKEN

DEFAULT_TIMEOUT = 5  # seconds
MAX_RETRIES = 2

def _post(payload):
    """
    Internal helper: gửi HTTP request với retry + timeout, có log chi tiết lỗi.
    """
    url    = "https://graph.facebook.com/v15.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}

    logging.info("📦 Đang gửi payload: %s", json.dumps(payload, indent=2))

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                url,
                params=params,
                json=payload,
                timeout=DEFAULT_TIMEOUT
            )

            if not resp.ok:
                logging.warning("⚠️ Facebook trả lỗi: %s", resp.text)

            resp.raise_for_status()
            data = resp.json()
            logging.info("✅ Gửi thành công: %s", data)
            return data
        except requests.exceptions.HTTPError as http_err:
            logging.error("❌ Lỗi HTTP: %s", http_err.response.text)
        except Exception as e:
            logging.warning("⚠️ Attempt %d/%d failed: %s", attempt, MAX_RETRIES, e)
            if attempt == MAX_RETRIES:
                logging.exception("❌ Tất cả retry đều thất bại")
                return None

def send_message(recipient_id, message_text, messaging_type="RESPONSE", persona_id=None):
    """
    Gửi tin nhắn văn bản thuần túy.
    """
    if not recipient_id:
        logging.error("❌ recipient_id trống — không thể gửi tin nhắn")
        return None

    payload = {
        "messaging_type": messaging_type,
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    if persona_id:
        payload["persona_id"] = persona_id

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
    Gửi template nâng cao (generic, button...) kèm optional text & quick replies.
    """
    if not recipient_id:
        logging.error("❌ recipient_id trống — không thể gửi template")
        return None

    if not text and not template_payload:
        logging.error("❌ Template phải có ít nhất 'text' hoặc 'template_payload'")
        return None

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

    return _post(payload)

def send_button_template(recipient_id, text, buttons, quick_replies=None, **kwargs):
    """
    Shortcut: gửi button template đơn giản.
    """
    if not text or not buttons:
        logging.error("❌ Button Template cần cả 'text' và 'buttons'")
        return None

    payload = {
        "template_type": "button",
        "text": text,
        "buttons": buttons
    }

    return send_template_message(
        recipient_id=recipient_id,
        text=text,
        template_payload=payload,
        quick_replies=quick_replies,
        **kwargs
    )
