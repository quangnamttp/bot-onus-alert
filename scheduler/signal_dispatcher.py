from core.signal_generator import generate_signals
from messages.format_signal import format_signal_batch
from messenger.registry_manager import load_user_status, is_approved_and_active

def send_regular_signals():
    signals = generate_signals()
    msg = format_signal_batch(signals)

    user_data = load_user_status()
    for user_id in user_data:
        if is_approved_and_active(user_id):
            send_message(user_id, msg)

def send_message(user_id, message):
    print(f"[signal_dispatcher] → {user_id}: {message}")
