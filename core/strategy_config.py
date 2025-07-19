class Strategy:
    def __init__(self, name, risk_ratio):
        self.name = name
        self.risk_ratio = risk_ratio

    def get_entry_price(self, coin):
        # mock giá đơn giản → sau này gắn API
        if self.name == "scalping":
            return 1000
        elif self.name == "swing":
            return 950
        else:
            return 980

def get_strategy():
    return Strategy(name="swing", risk_ratio=2.0)
