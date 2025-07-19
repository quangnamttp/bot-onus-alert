def tag_event(event_text):
    if "CPI" in event_text or "FOMC" in event_text:
        return "🔴 Cao"
    elif "NFP" in event_text or "Lãi suất" in event_text:
        return "🟠 Trung bình"
    else:
        return "🟢 Thấp"
