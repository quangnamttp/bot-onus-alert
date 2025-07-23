import requests

PAGE_ACCESS_TOKEN = "EAAUfsOzztLEBPKQKkm5BuLuBXMXzUfsEb6UZAfTZBRi8YZCkog3GlrcZB3EgGVfS3pGeO7s0s1x0nsWQBkyZCACE3fyl7dluU2rFu6raEk7rCPzDFQBHCwZChttww36WIKfQ6Ua3ZBpyNfCadOkG8AzCKfiIcbLAei8P7ql1b2eAnKITJohDpauAh0l0ZAZCesfusIJhyJRwveQZDZD"

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
