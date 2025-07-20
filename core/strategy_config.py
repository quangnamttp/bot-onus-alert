class Strategy:
    def __init__(self, name, risk_ratio):
        self.name = name
        self.risk_ratio = risk_ratio

    def get_entry_price(self, coin):
        return None  # tùy vào chiến thuật bạn có thể cài thêm

def get_strategy():
    return Strategy(name="Swing", risk_ratio=2.0)
