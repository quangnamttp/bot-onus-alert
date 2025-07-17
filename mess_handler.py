import os
import requests

def send_message(content, platform="Messenger"):
    if platform == "Messenger":
        url = "https://graph.facebook.com/v17.0/me/messages"
        payload = {
            "recipient": {"id": os.getenv("FB_RECIPIENT_ID")},
            "message": {"text": content}
        }
        headers = {
            "Authorization": f"Bearer {os.getenv('FB_PAGE_TOKEN')}",
            "Content-Type": "application/json"
        }
        r = requests.post(url, json=payload, headers=headers)
        print(f"[Messenger] ➤ Status: {r.status_code} → {content}")
    else:
        print(f"[{platform}] ➤ {content}")
