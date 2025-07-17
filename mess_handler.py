import os
import requests
import json

def load_recipients():
    try:
        with open("recipient_list.json") as f:
            data = json.load(f)
            return data.get("recipients", [])
    except Exception as e:
        print(f"⚠️ Không thể tải recipient list: {e}")
        return []

def send_message(content, platform="Messenger"):
    if platform == "Messenger":
        token = os.getenv("FB_PAGE_TOKEN")
        url = "https://graph.facebook.com/v17.0/me/messages"
        headers = {
            "Authorization": f"Bearer " + token,
            "Content-Type": "application/json"
        }
        for psid in load_recipients():
            payload = {
                "recipient": {"id": psid},
                "message": {"text": content}
            }
            r = requests.post(url, json=payload, headers=headers)
            print(f"[Messenger] ➤ {psid} → {r.status_code}: {content}")
    else:
        print(f"[{platform}] ➤ {content}")
