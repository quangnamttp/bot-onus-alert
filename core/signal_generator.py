from core.strategy_config import get_strategy
from core.risk_calculator import calc_tp_sl
from core.cache_manager import mark_used

def generate_signals(coins):
    strategy = get_strategy()
    signals = []

    for coin in coins:
        entry = strategy.get_entry_price(coin)
        tp, sl = calc_tp_sl(entry, strategy.risk_ratio)
        rr = round((tp - entry) / (entry - sl), 2)
        tag = "Tham khảo" if rr < 1.2 else "Xác suất cao"

        signal = {
            "coin": coin,
            "tp": tp,
            "sl": sl,
            "rr": rr,
            "tag": tag
        }
        signals.append(signal)
        mark_used(coin)

    return signals
