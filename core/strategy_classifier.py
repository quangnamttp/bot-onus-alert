def classify_strategy(rsi, funding):
    if rsi < 45 and funding < 0:
        return "Scalping"
    elif rsi > 50 and abs(funding) > 0.01:
        return "Swing"
    return "Scalping"
