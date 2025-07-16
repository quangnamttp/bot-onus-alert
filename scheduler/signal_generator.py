import random
from core.signal_analyzer import SignalAnalyzer
from core.strategy_classifier import classify_strategy
from core.risk_evaluator import evaluate_risk

def generate_signal(coin, exchange):
    analyzer = SignalAnalyzer(coin, exchange)
    indicators = analyzer.fetch_indicators()
    ma_position = "trên" if "trên" in indicators["MA"] else "dưới"
    strategy = classify_strategy(indicators["RSI"], ma_position, indicators["Volume"])

    entry = round(random.uniform(5.0, 100.0), 2)
    target = round(entry * 1.036, 2)
    stoploss = round(entry * 0.983, 2)
    rr = evaluate_risk(entry, stoploss)

    return (
        f"✅ #{coin.upper()} — {'LONG' if random.choice([True, False]) else 'SHORT'}\n"
        f"Sàn: {exchange} | Khung: M15\n\n"
        f"{analyzer.format_analysis()}\n\n"
        f"🎯 Entry: ${entry} | Target: ${target} | SL: ${stoploss}\n"
        f"📌 Chiến lược: {strategy}\n{rr}"
    )
