from macro.news_analyzer import analyze_macro_impact
from messenger.message_sender import send_message
import json

def evaluate_market_after_news(news_data):
    insight = analyze_macro_impact(news_data)

    with open("data/user_registry.json", "r") as f:
        users = json.load(f)

    for psid in users:
        send_message(psid, f"📈 Sau khi tin ra:\n{insight}")
