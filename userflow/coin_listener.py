# coin_listener.py

class CoinListener:
    def __init__(self):
        self.selected_coin = None

    def get_current_coin(self):
        if self.selected_coin:
            return self.selected_coin.upper()
        return "Chưa chọn coin nào"

    def update_coin(self, user_input):
        cleaned = user_input.strip().upper()
        blocked = ["BTCUP", "BTCDOWN", "ETH3L", "ETH3S", "DOGE5L", "SHIB1000"]
        if cleaned in blocked:
            return f"❌ '{cleaned}' bị chặn vì là token đòn bẩy hoặc coin rác"
        if not cleaned.isalnum():
            return f"❌ Coin không hợp lệ: '{cleaned}'"
        self.selected_coin = cleaned
        return f"✅ Đã ghi nhận: bạn muốn phân tích {self.selected_coin}"

    def reset_coin(self):
        self.selected_coin = None
        return "🔁 Bạn có thể chọn lại coin mới để phân tích"
