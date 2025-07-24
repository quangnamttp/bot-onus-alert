# cofure_bot/scheduler/news_schedule.py

import logging
from datetime import datetime
from utils.config_loader import TZ, DATETIME_FORMAT
from messenger.send_message import send_template_message
from utils.signal_switch import is_signal_enabled
from macro.forex_factory_fetcher import fetch_macro_news as fetch_macro_events

def send_macro_news(user_id, date="today", date_range=None, use_template=True):
    try:
        if not is_signal_enabled():
            logging.info("🔕 Bot đang OFF — không gửi lịch vĩ mô")
            return

        logging.info(f"📅 [Scheduler] Gửi lịch vĩ mô cho {date}")
        events = fetch_macro_events(date=date, date_range=date_range)
        logging.info(f"📊 Tổng số sự kiện nhận được: {len(events)}")

        filtered = []
        for evt in events:
            if not isinstance(evt, dict):
                continue
            impact = evt.get("impact", "").strip().lower()
            if impact in ["medium", "high", "very high", "trung bình", "cao", "rất cao"]:
                filtered.append(evt)

        if not filtered:
            ts = datetime.now(TZ).strftime(DATETIME_FORMAT)
            msg = f"🔔 Không có tin tức vĩ mô quan trọng hôm nay.\n🕒 Thời điểm kiểm tra: {ts}"
            send_template_message(user_id, "📅 Lịch vĩ mô", msg)
            logging.info("📤 Đã gửi: không có tin vĩ mô")
            return

        formatted = []
        for evt in filtered:
            time    = evt.get("time", "")[:5]
            country = evt.get("country", "🌐")
            event   = evt.get("title") or evt.get("event") or "Không rõ sự kiện"
            impact  = evt.get("impact", "Unknown")
            impact_level = impact.lower()
            emoji = {
                "rất cao": "🔴", "very high": "🔴",
                "cao": "🟠", "high": "🟠",
                "trung bình": "🟡", "medium": "🟡"
            }.get(impact_level, "⚪")
            formatted.append(f"{emoji} {time} - {country} - {event} ({impact})")

        now_str = datetime.now(TZ).strftime(DATETIME_FORMAT)
        content = f"📅 Lịch vĩ mô ngày {now_str}:\n\n" + "\n".join(formatted)
        send_template_message(user_id, "📅 Lịch vĩ mô hôm nay", content)
        logging.info("📤 Đã gửi bản tin vĩ mô thành công")

    except Exception as e:
        logging.exception(f"❌ Lỗi khi gửi lịch vĩ mô: {e}")
