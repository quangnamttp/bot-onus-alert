# cofure_bot/scheduler/morning_report.py

from messenger.send_message import send_message
from messages.greeting_format import morning_greeting
from marketdata.futures_tracker import get_price_data
from utils.config_loader import MY_USER_ID

def send_morning_report(user_id):
    prices = get_price_data()
    message = morning_greeting("Anh Trương", prices["BTC"], prices["ETH"], prices["SOL"])
    send_message(user_id, message)
