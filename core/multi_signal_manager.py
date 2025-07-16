# multi_signal_manager.py

from core.signal_analyzer import SignalAnalyzer
from core.strategy_classifier import classify_strategy
from utils.formatter import format_price, format_rr
from messages.templates import signal_template

def generate_batch_signals(coins, exchange):
    result = []
    for coin in coins:
        analyzer = SignalAnalyzer(coin, exchange)
        indicators = analyzer.fetch_indicators()

        ma_position = "trên" if "trên" in indicators["MA"] else "dưới"
        strategy = classify_strategy(indicators["RSI"], ma_position, indicators["Volume"])

        entry = round(indicators["Entry"], 2)
        target = round(entry * 1.036, 2)
        stoploss = round(entry * 0.983, 2)
        rr_text = f"📊 RR: {format_rr(entry, stoploss)}"

        signal = signal_template(
            coin, exchange, "LONG",
            format_price(entry), format_price(target),
            format_price(stoploss), strategy,
            analyzer.format_analysis(), rr_text
        )
        result.append(signal)
    return result
