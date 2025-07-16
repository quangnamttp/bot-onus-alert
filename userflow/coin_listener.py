from utils.validator import is_valid_coin

class CoinListener:
    def __init__(self):
        self.selected_coin = None

    def get_current_coin(self):
        if self.selected_coin:
            return self.selected_coin.upper()
        return "🤖 Bạn chưa chọn coin nào để phân tích"

    def update_coin(self, user_input):
        cleaned = user_input.strip().upper()
        if not is_valid_coin(cleaned):
            return f"❌ Coin '{cleaned}' không hợp lệ hoặc đã bị chặn"
        self.selected_coin = cleaned
        return f"✅ Đã ghi nhận: bạn muốn phân tích {self.selected_coin}"

    def reset_coin(self):
        self.selected_coin = None
        return "🔁 Coin đã được đặt lại — bạn có thể chọn coin khác!"
