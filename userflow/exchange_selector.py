# exchange_selector.py

class ExchangeSelector:
    def __init__(self):
        self.supported_exchanges = [
            "Binance", "OKX", "MEXC", "Nami", "Onus", "Bybit"
        ]
        self.selected_exchange = "Onus"  # ⚠️ Mặc định là ONUS

    def get_current_exchange(self):
        return self.selected_exchange

    def list_supported_exchanges(self):
        return self.supported_exchanges

    def update_exchange(self, user_input):
        formatted_input = user_input.strip().capitalize()
        for ex in self.supported_exchanges:
            if formatted_input.lower() == ex.lower():
                self.selected_exchange = ex
                return f"✅ Sàn giao dịch đã cập nhật thành: {self.selected_exchange}"
        return f"❌ Sàn '{user_input}' không được hỗ trợ. Chọn trong: {', '.join(self.supported_exchanges)}"
