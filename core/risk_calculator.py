def calc_tp_sl(entry, rr):
    tp = entry + (entry * 0.02 * rr)
    sl = entry - (entry * 0.01 * rr)
    return round(tp), round(sl)
