def mark_reference_signal(signal):
    if signal["rr"] < 1 or signal["risk"] > 3:
        signal["note"] = "📌 Tham khảo"
    return signal
