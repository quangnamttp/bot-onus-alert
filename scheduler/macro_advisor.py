from messenger.message_sender import send_message
from messenger.registry_manager import get_all_registered_users
from macro.news_analyzer import analyze_today_news

def check_macro_alerts():
    users = get_all_registered_users()
    news_alert = analyze_today_news()

    if not news_alert:
        return

    for psid in users:
        send_message(psid, f"🔔 Cảnh báo vĩ mô: {news_alert}")
