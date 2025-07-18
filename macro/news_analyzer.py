import requests
from messenger.message_sender import send_message
import json

def check_economic_events():
    url = "https://api.mock-investing.com/calendar/today"  # Giả lập
    events = requests.get(url).json()

    if events:
        with open("data/user_registry.json", "r") as f:
            users = json.load(f)

        for e in events:
            for psid in users:
                msg = f"📊 Lịch vĩ mô ra tin: {e['title']} lúc {e['time']}\nDự báo: {e['forecast']}"
                send_message(psid, msg)
