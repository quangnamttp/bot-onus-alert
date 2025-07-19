from core.strategy_config import get_strategy
from core.risk_calculator import calc_tp_sl
from core.cache_manager import mark_used
from core.signal_quality import evaluate_risk, check_entry_conditions

from market.indicator_reader import get_rsi
from market.volume_analyzer import get_volume
from market.funding_reader import get_funding
from market.price_reader import get_price

def generate_signals(coins):
    strategy = get_strategy()
    signals = []

    for coin in coins:
        entry = strategy.get_entry_price(coin) or get_price(coin)
        tp, sl = calc_tp_sl(entry, strategy.risk_ratio)
        rr = round((tp - entry) / (entry - sl), 2)

        # 📊 Đọc dữ liệu thị trường
        rsi = get_rsi(coin)
        volume = get_volume(coin)
        funding = get_funding(coin)

        # 🧠 Đánh giá độ rủi ro
        risk = evaluate_risk(rsi, volume, funding)

        # 🛠 Tạo tín hiệu
        signal = {
            "coin": coin,
            "entry": entry,
            "tp": tp,
            "sl": sl,
            "rr": rr,
            "risk": risk,
            "nr": 1,
            "strategy": strategy.name
        }

        # ✅ Kiểm tra điều kiện để gửi lệnh
        if not check_entry_conditions(signal):
            continue

        # 🏷️ Gắn tag đánh giá tín hiệu
        if risk == 3:
            signal["tag"] = "⚠️ Rủi ro cao"
        elif rr < 1.2:
            signal["tag"] = "Tham khảo"
        else:
            signal["tag"] = "Xác suất cao"

        signals.append(signal)
        mark_used(coin)

    return signals
