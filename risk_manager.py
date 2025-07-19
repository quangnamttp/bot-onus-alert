def calculate_targets(entry, strategy="scalping"):
    """
    Tính TP, SL và R:R dựa trên giá Entry.
    - Scalping: TP = +2%, SL = -1%
    - Swing:    TP = +4%, SL = -2%
    """
    if strategy == "swing":
        tp_ratio, sl_ratio = 0.04, 0.02
    else:
        tp_ratio, sl_ratio = 0.02, 0.01

    tp = round(entry * (1 + tp_ratio), 2)
    sl = round(entry * (1 - sl_ratio), 2)
    rr = round((tp - entry) / (entry - sl), 2)
    return {"tp": tp, "sl": sl, "rr": rr}
