# formatter.py

def format_price(value):
    return f"${value:,.2f}"

def format_vnd(value_usd, rate=24350):
    return f"{round(value_usd * rate):,} VNĐ"

def format_rr(entry, stoploss):
    distance = abs(entry - stoploss)
    rr = round((entry * 1.036 - entry) / distance, 2)
    return rr
