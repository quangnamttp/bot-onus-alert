def check_liquidity_zone(price, zones):
    for z in zones:
        if abs(price - z) / price < 0.01:
            return "💧 Gần vùng thanh khoản"
    return ""
