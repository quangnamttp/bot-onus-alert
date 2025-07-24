# cofure_bot/scheduler/news_schedule.py

import logging
from datetime import datetime
from utils.config_loader import TZ, DATETIME_FORMAT
from messenger.send_message import send_template_message
from utils.signal_switch import is_signal_enabled
from macro.forex_factory_fetcher import fetch_macro_news as fetch_macro_events
from macro.macro_advisor import generate_macro_strategy
from macro.news_analyzer import analyze_post_news  # ✅ Bổ sung hàm phân tích

def send_macro_news(user_id, date="today", date_range=None, use_template=True):
    try:
        if not is_signal_enabled():
            logging.info("🔕 Bot đang OFF — không gửi lịch vĩ mô")
            return

        logging.info(f"📅 [Scheduler] Gửi lịch vĩ mô cho {date}")
        events = fetch_macro_events(date=date, date_range=date_range)
        logging.info(f"📊 Tổng số sự kiện nhận được: {len(events)}")

        # 🎯 Lọc tin vĩ mô quan trọng
        filtered = []
        for evt in events:
            if not isinstance(evt, dict):
                continue
            impact = evt.get("impact", "").strip().lower()
            if impact in ["medium", "high", "very high", "trung bình", "cao", "rất cao"]:
                filtered.append(evt)

        # 🧠 Sinh chiến lược bản tin
        strategy_text = generate_macro_strategy(filtered, date_label="hôm nay")
        send_template_message(user_id, "📅 Chiến lược vĩ mô hôm nay", strategy_text)
        logging.info("📤 Đã gửi bản chiến lược vĩ mô")

        # 📊 Phân tích phản ứng thị trường (nếu có tin)
        if filtered:
            # 🧾 Lấy sự kiện đầu tiên làm ngữ cảnh (nếu cần)
            context = {
                "impact": filtered[0].get("impact", "medium"),
                "event_type": filtered[0].get("title", "").lower()
            }

            # 📈 Dữ liệu giả lập — bạn có thể thay bằng dữ liệu thực từ market API
            market_data = {
                "funding": 0.009,
                "volume": 41,
                "rsi": 58,
                "spread": 1.1
            }

            analysis = analyze_post_news(market_data, context)
            for line in analysis:
                send_template_message(user_id, "📊 Phản ứng thị trường sau tin", line)

            logging.info("📤 Đã gửi bản phân tích sau tin")

    except Exception as e:
        logging.exception(f"❌ Lỗi khi gửi lịch vĩ mô + phân tích: {e}")
