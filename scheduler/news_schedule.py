from macro.forex_factory_fetcher import fetch_macro_news
from macro.macro_advisor import generate_macro_strategy
from messenger.send_message import send_message
from utils.config_loader import MY_USER_ID

def send_macro_news(user_id, date="today", date_range=None):
    if date_range == "week":
        news = fetch_macro_news(date_range="week")
    elif date == "tomorrow":
        news = fetch_macro_news(date="tomorrow")
    elif date == "today":
        news = fetch_macro_news(date="today")
    else:
        news = []

    message = generate_macro_strategy(news)
    send_message(user_id, message)
