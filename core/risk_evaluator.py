# risk_evaluator.py

def evaluate_risk(entry, stoploss):
    distance = abs(entry - stoploss)
    rr_ratio = round((entry * 1.03 - entry) / distance, 2)
    if rr_ratio >= 2.0:
        risk = "Rủi ro thấp – RR tốt"
    elif rr_ratio >= 1.5:
        risk = "Rủi ro trung bình"
    else:
        risk = "Rủi ro cao"
    return f"📊 Tỷ lệ RR: {rr_ratio} | Đánh giá: {risk}"

