def calculate_sl_tp(entry_price, direction, strategy):
    buffer = 0.008 if strategy == "Scalping" else 0.015
    sl = entry_price * (1 - buffer) if direction == "BUY" else entry_price * (1 + buffer)
    tp1 = entry_price * (1 + buffer) if direction == "BUY" else entry_price * (1 - buffer)
    tp2 = entry_price * (1 + 2 * buffer) if direction == "BUY" else entry_price * (1 - 2 * buffer)
    
    return {
        "SL": round(sl, 2),
        "TP1": round(tp1, 2),
        "TP2": round(tp2, 2),
        "R_R": round((tp1 - entry_price) / (entry_price - sl), 2) if direction == "BUY"
        else round((entry_price - tp1) / (sl - entry_price), 2)
    }
