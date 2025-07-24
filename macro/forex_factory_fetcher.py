# macro/forex_factory_fetcher.py

import requests
import logging

# 🎯 Lọc tin có độ ảnh hưởng từ mức này trở lên
VALID_IMPACTS = [
    "medium", "high", "very high",
    "trung bình", "cao", "rất cao"
]

def is_macro_relevant(event):
    """
    Kiểm tra xem sự kiện có độ ảnh hưởng đủ mạnh để gửi bản tin
    """
    impact = event.get("impact", "").strip().lower()
    return impact in VALID_IMPACTS

def fetch_macro_news(date="today", date_range=None):
    """
    Gọi API forexfactory.ai để lấy tin vĩ mô theo ngày hoặc tuần
    """
    try:
        # 🌐 Xác định endpoint
        if date_range == "week":
            url = "https://api.forexfactory.ai/v1/week"
        elif date == "tomorrow":
            url = "https://api.forexfactory.ai/v1/tomorrow"
        else:
            url = "https://api.forexfactory.ai/v1/today"

        logging.info(f"📡 Đang fetch dữ liệu từ {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        news_data = response.json()

        # 🎯 Lọc tin đủ độ ảnh hưởng
        important_events = []
        for event in news_data.get("events", []):
            if is_macro_relevant(event):
                important_events.append({
                    "time": event.get("time", "⏰"),
                    "title": event.get("title", "Không rõ tiêu đề"),
                    "impact": event.get("impact", "Unknown")
                })

        logging.info(f"📊 Tổng số tin vĩ mô lọc được: {len(important_events)}")
        return important_events

    except Exception as e:
        logging.exception(f"❌ Lỗi fetch macro: {e}")
        return []
