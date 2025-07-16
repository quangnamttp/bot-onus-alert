# signal_generator.py

import random
from core.signal_analyzer import SignalAnalyzer
from core.strategy_classifier import classify_strategy
from core.risk_evaluator import evaluate_risk

def generate_signal(coin, exchange):
    analyzer = SignalAnalyzer(coin, exchange)
    indicators = analyzer.fetch_indicators()
    ma_position = "trên" if "trên" in indicators["MA"] else "dưới"
    strategy = classify_strategy(indicators["RSI"], ma_position, indicators["Volume"])
    
    entry = round(random.uniform(1.0, 100.0), 2)
    target = round(entry * 1.036, 2)
    stoploss = round(entry * 0.983, 2)
    
    rr = evaluate_risk(entry, stoploss)
    vn_price = f"{entry * 24350:,.0f} VNĐ"

    return (
        f"✅ #{coin.upper()} — {'LONG' if random.choice([True, False]) else 'SHORT'}\n"
        f"📍 Sàn: {exchange} | Khung giờ: M15\n\n"
        f"{analyzer.format_analysis()}\n\n"
        f"🎯 Entry: ${entry} ≈ {vn_price}\n"
        f"🎯 Target: ${target}\n"
        f"🛡️ Stop-Loss: ${stoploss}\n\n"
        f"📌 Chiến lược giao dịch: {strategy}\n{rr}"
    )

