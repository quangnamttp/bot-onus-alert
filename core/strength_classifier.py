def classify_strength(funding, volume, rsi, spread):
    score = 0

    # Đóng góp điểm từ volume (giới hạn 25)
    score += min(25, volume) * 0.8

    # Funding rate → càng cao càng mạnh (theo độ tuyệt đối)
    score += abs(funding) * 100

    # Đóng góp từ RSI:
    # - Nếu RSI > 50 → độ lệch × 0.6
    # - Nếu RSI < 50 → độ lệch × 0.4
    score += (rsi - 50) * 0.6 if rsi > 50 else (50 - rsi) * 0.4

    # Spread càng nhỏ → càng ưu thế tín hiệu
    score += 5 if spread < 0.9 else -5 if spread > 1.2 else 0

    # Giới hạn điểm từ 0 → 100 và gán nhãn
    strength = int(max(0, min(100, score)))
    label = (
        "RẤT MẠNH"    if strength >= 70 else
        "TIÊU CHUẨN"  if strength >= 50 else
        "THAM KHẢO"
    )

    return strength, label
