# cofure_bot/core/strength_classifier.py

def classify_strength(funding, volume, rsi, spread):
    score = 0

    score += min(25, volume) * 0.8
    score += abs(funding) * 100
    score += (rsi - 50) * 0.6 if rsi > 50 else (50 - rsi) * 0.4
    score += 5 if spread < 0.9 else -5 if spread > 1.2 else 0

    strength = int(max(0, min(100, score)))
    label = "RẤT MẠNH" if strength >= 70 else "TIÊU CHUẨN" if strength >= 50 else "THAM KHẢO"
    return strength, label
