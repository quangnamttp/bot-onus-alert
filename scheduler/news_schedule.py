# cofure_bot/scheduler/news_schedule.py

import logging
from macro.forex_factory_fetcher import fetch_macro_news
from macro.macro_advisor import generate_macro_strategy
from messenger.send_message import send_message, send_template_message

def send_macro_news(user_id, date="today", date_range=None, use_template=False):
    """
    Gửi lịch vĩ mô cho user:
      - Theo ngày (today, tomorrow) hoặc cả tuần (date_range="week")
      - Nếu use_template=True → gửi dưới dạng Generic Template interactive
      - Ngược lại → gửi text summary do generate_macro_strategy tạo
    """
    try:
        # 1. Fetch news theo tham số
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

        logging.info(f"📰 Fetched {len(news)} macro events {label}")

        # 2. Trường hợp không có news
        if not news:
            msg = f"🔕 Không có tin tức vĩ mô quan trọng {label}."
            send_message(user_id, msg)
            logging.info("📤 Sent no-news notification")
            return

        # 3a. Text mode: summary chiến lược
        if not use_template:
            message = generate_macro_strategy(news, date_label=label)
            send_message(user_id, message)
            logging.info("📤 Sent macro news as text")
            return

        # 3b. Template mode: build Generic Template elements
        elements = []
        for item in news:
            time_str = item.get("time", "")
            curr     = item.get("currency", "")
            event    = item.get("event", "")
            impact   = item.get("impact", "Medium")  # High/Medium/Low
            emoji    = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}.get(impact, "⚪️")
            title    = f"{time_str} – {curr} – {event}"
            subtitle = f"{emoji} Tác động: {impact}"

            # Nút “Chi tiết” mở link gốc
            btn = {
                "type": "web_url",
                "url": item.get("url", ""),
                "title": "📄 Chi tiết"
            }

            elements.append({
                "title": title,
                "subtitle": subtitle,
                "buttons": [btn]
            })

        # Messenger chỉ hiển thị tối đa 10 cards
        payload = {
            "template_type": "generic",
            "elements": elements[:10]
        }

        logging.info("📋 Sending macro news as Generic Template")
        send_template_message(
            recipient_id=user_id,
            text=f"📅 Lịch vĩ mô {label}:",
            template_payload=payload
        )
        logging.info("📤 Sent macro news as template")

    except Exception:
        logging.exception("❌ Lỗi khi gửi lịch vĩ mô")
