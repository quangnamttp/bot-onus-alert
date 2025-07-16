# emoji_map.py

def get_coin_emoji(coin):
    emojis = {
        "BTC": "₿", "ETH": "⚙️", "SOL": "🔥", "XRP": "💧", "DOGE": "🐶"
    }
    return emojis.get(coin.upper(), "📈")

def get_strategy_emoji(strategy):
    return "⚡" if "Scalp" in strategy else "🕰️"
