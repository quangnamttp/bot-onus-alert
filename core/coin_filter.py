from core.cache_manager import is_used
from market.volume_analyzer import get_volume
from market.funding_reader import get_funding
from market.price_reader import get_price

def is_market_strong(coin):
    volume = get_volume(coin)
    funding = get_funding(coin)
    price = get_price(coin)

    conditions = [
        volume > 300000,
        abs(funding) > 0.015,
        price > 10000
    ]
    return sum(conditions) >= 2

def filter_coins(raw_list):
    filtered = []
    for coin in raw_list:
        if is_used(coin) and not is_market_strong(coin):
            continue
        volume = get_volume(coin)
        price = get_price(coin)
        if volume > 100000 and price > 10000:
            filtered.append(coin)
    return filtered
