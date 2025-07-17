def check_entry_conditions(signal):
    if signal["rr"] >= 1 and signal["risk"] <= 2:
        return True
    return False
