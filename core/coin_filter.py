from market.volume_analyzer import get_top_volume_coins
from market.funding_reader import get_funding_rates
from market.volatility_checker import get_volatility_score
from core.cache_manager import get_used_today

def get_filtered_coins():
    volume_coins = get_top_volume_coins(limit=10)
    funding = get_funding_rates()
    volatility = get_volatility_score()
    used = get_used_today()

    candidates = []
    for coin in volume_coins:
        if coin in used:
            continue
        if volatility[coin] < 2.0:
            continue
        if abs(funding[coin]) > 0.06:
            continue
        candidates.append(coin)

    return candidates
