def classify_strength(volume, spread):
    v_score = volume["change"]
    bias = volume["bias"]
    rsi = spread["rsi"]
    tightness = spread["tightness"]

    score = 0
    score += min(v_score / 2, 30)
    score += 10 if bias in ["Long", "Short"] else 0
    score += 10 if rsi > 60 or rsi < 40 else 0
    score += 10 if tightness == "co" else 0

    return int(score)
