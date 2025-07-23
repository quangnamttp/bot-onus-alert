import requests

PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"

def send_message(recipient_id, message_text):
    payload = {
        "recipient": { "id": recipient_id },
        "message": { "text": message_text }
    }
    headers = {
        "Content-Type": "application/json"
    }
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.post(url, json=payload, headers=headers)
    print(f"[send_message] → {recipient_id}: {message_text} | Status: {response.status_code}")
