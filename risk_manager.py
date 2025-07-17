def calc_sl_tp(entry, sl_percent, tp_percent):
    sl = entry * (1 - sl_percent)
    tp = entry * (1 + tp_percent)
    return round(sl, 2), round(tp, 2)
