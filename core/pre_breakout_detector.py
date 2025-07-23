# cofure_bot/core/pre_breakout_detector.py

def detect_pattern(symbol):
    # Logic đơn giản demo: có thể thay bằng phân tích nến / volume cụ thể
    if symbol in ["KAI", "CHI", "MAV"]:
        return "tam giác tăng"
    elif symbol == "RACA":
        return "vai đầu vai"
    else:
        return "nền phẳng"
