# cofure_bot/scheduler/news_schedule.py

import logging
from datetime import datetime
from utils.config_loader import TZ, DATETIME_FORMAT
from messenger.send_message import send_template_message
from utils.signal_switch import is_signal_enabled

# ⚠️ Giả định: bạn có hàm fetch_macro_events(date) → trả về list[dict]
from core.news_data_source import fetch_macro_events

def send_macro_news(user_id, date="today", date_range=None, use_template=True):
    try:
        if not is_signal_enabled():
            logging.info("🔕 Bot đang OFF — không gửi lịch vĩ mô")
            return

        logging.info(f"📅 [Scheduler] Gửi lịch vĩ mô cho {date}")
        events = fetch_macro_events(date=date, range=date_range)
        logging.info(f"📊 Tổng số sự kiện nhận được: {len(events)}")

        filtered = []
        for evt in events:
            impact = evt.get("impact", "").strip().lower()
            if impact in ["medium", "high", "very high", "trung bình", "cao", "rất cao"]:
                filtered.append(evt)

        if not filtered:
            ts = datetime.now(TZ).strftime(DATETIME_FORMAT)
            msg = f"🔔 Không có tin tức vĩ mô quan trọng hôm nay.\n🕒 Thời điểm kiểm tra: {ts}"
            send_template_message(user_id, "📅 Lịch vĩ mô", msg)
            logging.info("📤 Đã gửi: không có tin vĩ mô")
            return

        # 🧾 Format nội dung bản tin
        formatted = []
        for evt in filtered:
            time = evt.get("time", "")[:5]
            country = evt.get("country", "")
            event = evt.get("event", "")
            impact = evt.get("impact", "")
            emoji = "🔴" if "very" in impact.lower() or "rất" in impact.lower() else \
                    "🟠" if "high" in impact.lower() or "cao" in impact.lower() else \
                    "🟡"
            formatted.append(f"{emoji} {time} - {country} - {event} ({impact})")

        now_str = datetime.now(TZ).strftime(DATETIME_FORMAT)
        content = f"📅 Lịch vĩ mô ngày {now_str}:\n\n" + "\n".join(formatted)
        send_template_message(user_id, "📅 Lịch vĩ mô hôm nay", content)
        logging.info("📤 Đã gửi bản tin vĩ mô thành công")

    except Exception:
        logging.exception("❌ Lỗi khi gửi lịch vĩ mô")
