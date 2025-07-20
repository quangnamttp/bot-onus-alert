import json

CACHE_PATH = "data/used_coins.json"

def get_used_today():
    try:
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def mark_used(coin):
    try:
        used = get_used_today()
        if coin not in used:
            used.append(coin)
            with open(CACHE_PATH, "w") as f:
                json.dump(used, f, indent=2)
    except:
        pass

def reset_coin_state():
    with open(CACHE_PATH, "w") as f:
        json.dump([], f)

def is_used(coin):
    return coin in get_used_today()
