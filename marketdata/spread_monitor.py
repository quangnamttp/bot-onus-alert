import random

def get_spread_data():
    coins = get_all_futures()
    result = {}
    for coin in coins:
        result[coin] = {
            "rsi": random.randint(45, 75),
            "bias": "Long" if random.random() < 0.5 else "Short",
            "tightness": "co" if random.random() < 0.6 else "loose",
            "price": random.randint(12_000, 28_000),
            "target_range": 400,
            "risk_range": 200
        }
    return result

def detect_spread_spike():
    coins = get_all_futures()
    result = {}
    for coin in coins:
        rsi = random.randint(70, 90)
        result[coin] = {
            "rsi": rsi,
            "bias": "Long" if rsi > 75 else "Short",
            "price": random.randint(12_000, 28_000)
        }
    return result

def check_pinbar_rsi(coin):
    return {
        "rsi": random.randint(55, 65),
        "pinbar": True,
        "bias": "Long",
        "entry": random.randint(15_000, 18_000)
    }
