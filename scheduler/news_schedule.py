from macro.forex_factory_fetcher import get_today_news
from messenger.registry_manager import load_user_status, is_approved_and_active

def send_daily_news_schedule():
    news_list = get_today_news()
    if not news_list:
        news_msg = "📅 Hôm nay không có tin tức vĩ mô quan trọng.\nChúc bạn một ngày trade thật thành công nha!"
    else:
        news_msg = "📅 Lịch tin vĩ mô hôm nay:\n" + "\n".join([
            f"🕒 {n['time']} • {n['title']} • Ảnh hưởng: {n['impact']}" for n in news_list
        ])

    user_data = load_user_status()
    for user_id in user_data:
        if is_approved_and_active(user_id):
            send_message(user_id, news_msg)

def send_message(user_id, message):
    print(f"[news_schedule] → {user_id}: {message}")
