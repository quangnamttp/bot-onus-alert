# signal_engine.py
from market_data import get_all_symbols, get_kline, get_rsi, get_price, get_volume

def scan_entry():
    """Quét thị trường và trả về các tín hiệu LONG/SHORT tiềm năng"""
    signals = []

    for symbol in get_all_symbols():
        try:
            candles = get_kline(symbol)
            rsi = get_rsi(candles)
            close_price = float(candles[-1][4])
            ma20 = sum([float(k[4]) for k in candles[-20:]]) / 20
            volume = get_volume(symbol)
            signal = None

            # Điều kiện vào lệnh LONG
            if rsi < 30 and close_price > ma20:
                signal = {
                    "type": "LONG",
                    "symbol": symbol,
                    "price": close_price,
                    "rsi": rsi,
                    "ma20": round(ma20, 4),
                    "volume": round(volume, 2),
                    "tp": round(close_price * 1.05, 4),
                    "sl": round(close_price * 0.95, 4),
                    "entry_type": "market"
                }

            # Điều kiện vào lệnh SHORT
            if rsi > 70 and close_price < ma20:
                signal = {
                    "type": "SHORT",
                    "symbol": symbol,
                    "price": close_price,
                    "rsi": rsi,
                    "ma20": round(ma20, 4),
                    "volume": round(volume, 2),
                    "tp": round(close_price * 0.95, 4),
                    "sl": round(close_price * 1.05, 4),
                    "entry_type": "market"
                }

            if signal:
                signals.append(signal)

        except Exception as e:
            print(f"🚫 {symbol} lỗi khi phân tích: {e}")
            continue

    return signals
