# event_watcher.py

def notify_event(time_now):
    if time_now == "19:30":
        return (
            "⏳ Sắp ra tin CPI Hoa Kỳ (19:30)\n"
            "→ Tránh mở lệnh mới trước tin\n"
            "→ Canh phản ứng sau tin để xác nhận xu hướng!"
        )
    return None
