def detect_liquidity_zones(price, recent_levels):
    zones = []
    for level in recent_levels:
        if abs(price - level) / price < 0.01:
            zones.append(level)
    return zones
