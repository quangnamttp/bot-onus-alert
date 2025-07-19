from utils.signal_tracker import clear_stats
from core.cache_manager import reset_coin_state

def reset_all_data():
    clear_stats()
    reset_coin_state()
