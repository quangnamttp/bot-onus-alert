def analyze_market(rsi, funding, change):
    if rsi >= 40 and abs(funding) <= 0.02 and abs(change) >= 3:
        return True
    return False
