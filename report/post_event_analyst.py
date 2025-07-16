# post_event_analyst.py

def analyze_after_event(coin, exchange, rsi, volume, reaction_direction):
    coin = coin.upper()
    bias = "MUA" if reaction_direction == "up" else "BÁN"

    return (
        f"📉 Phân tích sau tin vĩ mô\n"
        f"Coin: {coin} | Sàn: {exchange}\n"
        f"→ RSI hiện tại: {rsi} | Volume bật lên: {volume:,} USDT\n"
        f"→ Phản ứng giá theo chiều: {bias}\n\n"
        f"📌 Chiến lược đề xuất:\n"
        f"- Ưu tiên {'Scalp LONG' if bias == 'MUA' else 'Scalp SHORT'} trong 1–2 tiếng sau tin\n"
        f"- Đặt SL gần vùng biến động | Không giữ lệnh qua đêm nếu tin còn dư âm"
    )
