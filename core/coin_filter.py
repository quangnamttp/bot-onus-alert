from config import MIN_VOLUME, JUNK_COINS

def is_junk_coin(symbol):
    return symbol in JUNK_COINS

def is_valid_coin(symbol, volume):
    return volume >= MIN_VOLUME and not is_junk_coin(symbol)
