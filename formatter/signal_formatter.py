def format_signal(signal, price_usdt, vnd_rate):
    price_vnd = price_usdt * vnd_rate
    return f"{signal} ({round(price_vnd):,} VNĐ)"

