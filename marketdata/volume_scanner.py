import random

def get_volume_data():
    coins = get_all_futures()
    result = {}
    for coin in coins:
        volume = random.randint(5, 50)
        result[coin] = {
            "change": volume,            # phần trăm thay đổi volume
            "bias": "Long" if volume % 2 == 0 else "Short"
        }
    return result

def get_surge_volume():
    # Quét những coin có volume tăng bất thường → sinh lệnh khẩn
    coins = get_all_futures()
    result = {}
    for coin in coins:
        surge = random.randint(30, 80)
        if surge > 50:
            result[coin] = {
                "change": surge,
                "bias": "Long" if surge % 2 == 0 else "Short"
            }
    return result

def get_accumulating_coins():
    coins = get_all_futures()
    return [c for c in coins if random.random() < 0.3]
