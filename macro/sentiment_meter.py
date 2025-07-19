def get_sentiment_from_data(btc_change_pct, alt_volatility):
    if btc_change_pct > 2 and alt_volatility > 4:
        return "🟢 Lạc quan (Bullish)"
    elif btc_change_pct < -2 and alt_volatility > 3:
        return "🔴 Bi quan (Bearish)"
    else:
        return "🟠 Trung lập"
