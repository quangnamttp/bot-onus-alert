def calc_tp_sl(entry, rr):
    tp = int(entry * (1 + rr * 0.01))
    sl = int(entry * (1 - 0.01 * rr * 0.6))
    return tp, sl
