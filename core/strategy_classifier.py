# strategy_classifier.py

def classify_strategy(rsi, ma_position, volume):
    if rsi >= 70 and ma_position == "trên":
        return "Scalping Trade"
    elif rsi <= 35 and volume > 2_000_000:
        return "Swing Trade"
    elif 40 <= rsi <= 60:
        return "Swing Trade"
    else:
        return "Scalping Trade"
