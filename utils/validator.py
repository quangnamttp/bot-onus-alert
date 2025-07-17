def validate_signal(signal):
    required_keys = ["symbol", "entry", "sl", "tp", "strategy", "rr"]
    return all(k in signal and signal[k] is not None for k in required_keys)

def validate_price(price):
    return isinstance(price, (int, float)) and price > 0

def validate_percent(value):
    return isinstance(value, float) and 0 <= value <= 1
