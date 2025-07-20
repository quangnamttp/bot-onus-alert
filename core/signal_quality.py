def evaluate_risk(rsi, volume, funding):
    score = 0
    if rsi < 30 or rsi > 70:
        score += 1
    if volume < 200000:
        score += 1
    if abs(funding) > 0.03:
        score += 1
    return score

def check_entry_conditions(signal):
    return signal.get("nr", 1) >= 1 and signal.get("risk", 0) <= 2
