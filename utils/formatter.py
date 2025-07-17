def format_price(price):
    return f"{price:,.0f} VND"

def format_percent(value):
    return f"{round(value * 100, 1)}%"

def format_rr(ratio):
    return f"{round(ratio, 2)}"
