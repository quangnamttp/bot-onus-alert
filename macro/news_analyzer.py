# cofure_bot/macro/news_analyzer.py

def analyze_post_news(market_data):
    funding = market_data["funding"]
    volume = market_data["volume"]
    rsi = market_data["rsi"]
    spread = market_data["spread"]

    signals = []
    if funding > 0.008 and volume > 30 and rsi > 55:
        signals.append("Thị trường phản ứng tích cực → có thể Long")
    elif funding < -0.008 and rsi < 45 and spread > 1.3:
        signals.append("Thị trường phản ứng tiêu cực → nên đứng ngoài")

    return signals
