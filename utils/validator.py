# validator.py

from config import SUPPORTED_EXCHANGES, BLOCKED_COINS

def is_valid_coin(coin):
    """
    Kiểm tra xem coin có hợp lệ không (không phải mã rác, mã đòn bẩy)
    """
    coin = coin.upper()
    return coin.isalnum() and coin not in BLOCKED_COINS

def is_valid_exchange(exchange):
    """
    Kiểm tra xem sàn có nằm trong danh sách được hỗ trợ không
    """
    return exchange.capitalize() in SUPPORTED_EXCHANGES
