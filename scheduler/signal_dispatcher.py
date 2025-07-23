from messenger.send_message import send_message
from messenger.registry_manager import load_user_status, is_approved_and_active
from messages.format_signal import format_signal

def loop_send_trade_signals():
    users = load_user_status()

    signal = {
        "coin": "BTC",
        "entry": "63,200",
        "tp": "64,900",
        "sl": "62,400",
        "strength": 78,
        "reason": "Funding lệch Long + volume breakout",
        "strategy": "Swing",
        "order_type": "Limit"
    }

    message = format_signal(signal)

    for user_id, info in users.items():
        if is_approved_and_active(user_id):
            send_message(user_id, message)
