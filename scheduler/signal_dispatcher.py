# cofure_bot/scheduler/signal_dispatcher.py

from core.signal_generator import generate_signals
from messages.format_signal import format_signal_batch
from messenger.send_message import send_message
from utils.config_loader import MY_USER_ID

def send_trade_signals(user_id):
    signals = generate_signals()
    formatted = format_signal_batch(signals)
    send_message(user_id, formatted)
