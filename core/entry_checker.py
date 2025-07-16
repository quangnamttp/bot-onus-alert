# entry_checker.py

def validate_trade(entry, target, stoploss):
    """
    Kiểm tra thông số lệnh trước khi gửi tín hiệu
    """
    if entry <= 0 or target <= 0 or stoploss <= 0:
        return False, "❌ Giá trị phải lớn hơn 0"

    if not (stoploss < entry < target or target < entry < stoploss):
        return False, "❌ Entry phải nằm giữa TP và SL"

    rr = round(abs(target - entry) / abs(entry - stoploss), 2)
    if rr < 1.0:
        return False, f"⚠️ Tỷ lệ RR thấp ({rr}) — cần xem lại vị trí vào lệnh"

    return True, f"✅ Lệnh hợp lệ | RR: {rr}"
