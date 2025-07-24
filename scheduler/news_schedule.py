# cofure_bot/scheduler/news_schedule.py

import logging
from datetime import datetime
from utils.config_loader import TZ, DATETIME_FORMAT
from messenger.send_message import send_template_message
from utils.signal_switch import is_signal_enabled
from macro.forex_factory_fetcher import fetch_macro_news as fetch_macro_events
from macro.macro_advisor import generate_macro_strategy

def send_macro_news(user_id, date="today", date_range=None, use_template=True):
    try:
        if not is_signal_enabled():
            logging.info("🔕 Bot đang OFF — không gửi lịch vĩ mô")
            return

        logging.info(f"📅 [Scheduler] Gửi lịch vĩ mô cho {date}")
        events = fetch_macro_events(date=date, date_range=date_range)
        logging.info(f"📊 Tổng số sự kiện nhận được: {len(events)}")

        # 🎯 Chỉ giữ tin có độ ảnh hưởng từ “Trung bình” trở lên
        filtered = []
        for evt in events:
            if not isinstance(evt, dict):
                continue
            impact = evt.get("impact", "").strip().lower()
            if impact in ["medium", "high", "very high", "trung bình", "cao", "rất cao"]:
                filtered.append(evt)

        # 🧠 Gọi hàm sinh chiến lược (tự xử lý cả khi không có tin)
        strategy_text = generate_macro_strategy(filtered, date_label="hôm nay")
        send_template_message(user_id, "📅 Chiến lược vĩ mô hôm nay", strategy_text)
        logging.info("📤 Đã gửi bản tin chiến lược vĩ mô thành công")

    except Exception as e:
        logging.exception(f"❌ Lỗi khi gửi lịch vĩ mô: {e}")
