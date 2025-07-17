def calc_sl_tp(entry, sl_percent=0.01, tp_percent=0.012):
    sl = entry * (1 - sl_percent)
    tp = entry * (1 + tp_percent)
    return round(sl, 2), round(tp, 2)
