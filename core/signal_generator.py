import logging
from marketdata.futures_tracker import get_futures_data
from core.strength_classifier import classify_strength
from core.pre_breakout_detector import detect_pattern

def generate_signals(max_signals=5):
    coin_data = get_futures_data()
    logging.info(f"📦 Dữ liệu nhận được: {len(coin_data)} coins")
    signals = []

    for coin in coin_data:
        fund = coin["funding"]
        vol = coin["volume_change"]
        rsi = coin["rsi"]
        spread = coin["spread"]
        price = coin["price"]
        symbol = coin["symbol"]
        pattern = detect_pattern(symbol)

        strength, label = classify_strength(fund, vol, rsi, spread)

        logging.info(f"🔍 {symbol} → fund={fund}, rsi={rsi}, pattern={pattern}, spread={spread}")

        direction = None
        if fund > 0.004 and rsi > 52 and pattern in ["tam giác tăng", "nền phẳng", "breakout"]:
            direction = "Long"
        elif fund < -0.004 and rsi < 48 and pattern in ["vai đầu vai", "nền giảm", "cờ giảm"]:
            direction = "Short"
        else:
            logging.info(f"⛔ Loại {symbol} — không thỏa điều kiện logic")
            continue

        if abs(spread) > 2.0:
            logging.info(f"⛔ Loại {symbol} — spread quá cao ({spread})")
            continue

        signal = {
            "symbol": symbol,
            "order_type": "Market",
            "strategy": "Scalping" if len(signals) < 3 else "Swing",
            "side": direction,
            "entry": price,
            "tp": price * 1.07 if direction == "Long" else price * 0.93,
            "sl": price * 0.95 if direction == "Long" else price * 1.05,
            "funding": fund,
            "volume_change": vol,
            "rsi": rsi,
            "spread": spread,
            "pattern": pattern,
            "strength": strength,
            "strength_label": label,
            "session_time": "Real-time"
        }

        signals.append(signal)
        logging.info(f"📡 Tín hiệu tạo thành: {symbol} {direction} ✅")

        if len(signals) >= max_signals:
            break

    if not signals:
        logging.warning("🚨 Không có tín hiệu nào được tạo — kiểm tra lại dữ liệu & điều kiện lọc!")

    logging.info(f"📊 Tổng số tín hiệu được chọn: {len(signals)}")
    return signals
