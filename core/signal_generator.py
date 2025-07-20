from core.strategy_config import get_strategy
from core.risk_calculator import calc_tp_sl
from core.cache_manager import mark_used, is_used
from core.signal_quality import evaluate_risk, check_entry_conditions

from market.indicator_reader import get_rsi
from market.volume_analyzer import get_volume
from market.funding_reader import get_funding
from market.price_reader import get_price

def generate_signals(coins):
    strategy = get_strategy()
    signals = []

    for coin in coins:
        if is_used(coin):
            continue

        entry = strategy.get_entry_price(coin) or get_price(coin)
        tp, sl = calc_tp_sl(entry, strategy.risk_ratio)
        rr = round((tp - entry) / (entry - sl), 2)

        rsi = get_rsi(coin)
        volume = get_volume(coin)
        funding = get_funding(coin)
        risk = evaluate_risk(rsi, volume, funding)

        signal = {
            "coin": coin,
            "entry": entry,
            "tp": tp,
            "sl": sl,
            "rr": rr,
            "risk": risk,
            "nr": 1,
            "strategy": strategy.name,
            "rsi": rsi,
            "volume": volume,
            "funding": funding
        }

        if not check_entry_conditions(signal):
            continue

        if risk == 3:
            signal["tag"] = "⚠️ Rủi ro cao"
        elif rr < 1.2:
            signal["tag"] = "Tham khảo"
        else:
            signal["tag"] = "Xác suất cao"

        signals.append(signal)
        mark_used(coin)

    return signals
