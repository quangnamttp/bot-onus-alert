from macro.forex_factory_fetcher import fetch_macro_news
from macro.macro_advisor import generate_macro_strategy
from messenger.send_message import send_message
from utils.config_loader import MY_USER_ID

def send_macro_news(user_id, date="today", date_range=None):
    # 📊 Lấy tin theo ngày hoặc cả tuần
    if date_range == "week":
        news = fetch_macro_news(date_range="week")
        label = "trong tuần"
    elif date == "tomorrow":
        news = fetch_macro_news(date="tomorrow")
        label = "ngày mai"
    elif date == "today":
        news = fetch_macro_news(date="today")
        label = "hôm nay"
    else:
        news = []
        label = "đã chọn"

    # 🧠 Tạo nội dung bản tin với nhãn thời gian tương ứng
    message = generate_macro_strategy(news, date_label=label)
    send_message(user_id, message)
