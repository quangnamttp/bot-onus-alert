def calculate_position_size(balance_usdt, risk_pct, entry_price, stop_loss_price):
    risk_amount = balance_usdt * (risk_pct / 100)
    stop_loss_distance = abs(entry_price - stop_loss_price)
    position_size = risk_amount / stop_loss_distance if stop_loss_distance else 0
    return round(position_size, 2)

def recommend_risk_level(rsi, volatility_pct):
    if rsi < 35 and volatility_pct > 3:
        return "⚠️ Cảnh báo: biến động mạnh, nên giữ rủi ro dưới 1%"
    elif rsi > 70:
        return "📌 Tín hiệu quá mua: rủi ro vừa phải (1.5%–2%)"
    return "✅ Rủi ro ổn định: có thể dùng 2% vốn giao dịch"

