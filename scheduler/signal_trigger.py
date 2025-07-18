from core.signal_generator import generate_signals
from messenger.message_sender import send_message
import json

def trigger_scheduled_signals():
    with open("data/user_registry.json", "r") as f:
        users = json.load(f)

    signals = generate_signals()

    for psid in users:
        for signal in signals:
            send_message(psid, f"📢 Tín hiệu mới: {signal}")
