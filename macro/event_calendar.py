import datetime

def get_today_events():
    today = datetime.date.today().strftime("%Y-%m-%d")
    # Dữ liệu mẫu — sau này thay bằng crawler hoặc API
    events = {
        "2025-07-19": ["🇺🇸 CPI Mỹ 19:30", "🇯🇵 Lãi suất BOJ 11:00"],
        "2025-07-20": ["🇺🇸 FOMC Minutes 01:00 sáng"],
    }
    return "\n".join(events.get(today, []))
