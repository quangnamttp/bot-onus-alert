# marketdata/liquidity_detector.py

import random

def detect_liquidity_spike(coin):
    coin = coin.upper()

    recent_volume = random.randint(3_000_000, 9_000_000)
    avg_volume = random.randint(500_000, 2_000_000)
    rsi = random.randint(45, 80)
    price_now = round(random.uniform(145, 150), 2)
    price_before = round(price_now - random.uniform(1.0, 2.5), 2)

    if recent_volume > avg_volume * 3:
        direction = "mua mạnh" if rsi >= 60 else "xả mạnh"
        suggestion = "Scalp theo chiều tăng" if rsi >= 60 else "Scalp theo chiều giảm"
        sl = round(price_now - 1.3, 2) if rsi >= 60 else round(price_now + 1.2, 2)

        return (
            f"⚡ DÒNG TIỀN BẤT THƯỜNG PHÁT HIỆN ⚡\n\n"
            f"#{coin} | Volume {direction} tăng {recent_volume // 1000}K USDT trong 3 phút qua\n"
            f"RSI bật mạnh: {rsi} | Giá đẩy từ ${price_before} → ${price_now}\n\n"
            f"→ Gợi ý: {suggestion} | Đặt SL: ${sl}"
        )
    return None
