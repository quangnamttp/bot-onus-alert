def generate_entry_signal(coin, rsi, volume_change, price):
    if volume_change >= 2.5 and rsi > 55:
        return f"💥 {coin} dòng tiền mạnh → canh LONG tại {price}"
    elif volume_change >= 2.5 and rsi < 45:
        return f"⚠️ {coin} dòng tiền vào nhưng RSI yếu → cân nhắc SHORT {price}"
    else:
        return f"📌 {coin} chưa rõ dòng tiền → đứng ngoài tại {price}"

