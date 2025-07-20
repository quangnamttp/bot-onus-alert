from core.entry_formatter import format_vnd

def explain_market_conditions(rsi, volume, funding):
    parts = []
    if rsi < 30:
        parts.append("RSI đang ở vùng quá bán")
    elif rsi > 70:
        parts.append("RSI đang ở vùng quá mua")
    else:
        parts.append("RSI trung tính")

    if volume > 250000:
        parts.append("volume tăng dần")
    elif volume < 100000:
        parts.append("volume thấp")
    else:
        parts.append("volume trung bình")

    if funding > 0.01:
        parts.append("funding lệch về chiều long")
    elif funding < -0.01:
        parts.append("funding lệch về chiều short")
    else:
        parts.append("funding trung lập")

    return ", ".join(parts)

def estimate_probability(rr, risk):
    base = min(rr, 2.5) / 2.5 * 100
    penalty = risk * 12
    return max(base - penalty, 30)

def format_signal_message(signal):
    coin = signal["coin"]
    strategy = signal["strategy"]
    entry_type = "Market" if signal["rr"] >= 1.5 else "Limit"

    entry = format_vnd(signal["entry"])
    tp = format_vnd(signal["tp"])
    sl = format_vnd(signal["sl"])
    rr = signal["rr"]
    tag = signal.get("tag", "Tham khảo")

    rsi = signal.get("rsi", 50)
    volume = signal.get("volume", 200000)
    funding = signal.get("funding", 0)

    reason = explain_market_conditions(rsi, volume, funding)
    probability = estimate_probability(rr, signal["risk"])

    return (
        f"📌 Lệnh cho: {coin} ({strategy})\n\n"
        f"💬 Lý do vào lệnh:\n{reason}\n\n"
        f"🎯 Giá vào lệnh: {entry}\n"
        f"🔁 Loại lệnh: {entry_type}\n\n"
        f"🎯 TP: {tp}\n"
        f"🛡️ SL: {sl}\n"
        f"⚖️ Risk/Reward: {rr}\n\n"
        f"🔍 Đánh giá tín hiệu: {tag}\n"
        f"📊 Tỉ lệ vào lệnh: **{round(probability)}%**"
    )
