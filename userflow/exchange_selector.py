from utils.validator import is_valid_exchange
from config import SUPPORTED_EXCHANGES

class ExchangeSelector:
    def __init__(self):
        self.selected_exchange = "Onus"  # sàn mặc định

    def get_current_exchange(self):
        return self.selected_exchange

    def list_supported_exchanges(self):
        return SUPPORTED_EXCHANGES

    def update_exchange(self, user_input):
        formatted = user_input.strip().capitalize()
        if is_valid_exchange(formatted):
            self.selected_exchange = formatted
            return f"✅ Sàn giao dịch đã cập nhật: {self.selected_exchange}"
        return (
            f"❌ Sàn '{user_input}' không được hỗ trợ\n"
            f"→ Các sàn hợp lệ gồm: {', '.join(SUPPORTED_EXCHANGES)}"
        )
