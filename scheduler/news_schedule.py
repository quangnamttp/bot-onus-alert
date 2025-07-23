# cofure_bot/scheduler/news_schedule.py

from macro.forex_factory_fetcher import fetch_macro_news
from macro.macro_advisor import generate_macro_strategy
from messenger.send_message import send_message
from utils.config_loader import MY_USER_ID

def send_macro_news(user_id):
    news = fetch_macro_news()
    message = generate_macro_strategy(news)
    send_message(user_id, message)
