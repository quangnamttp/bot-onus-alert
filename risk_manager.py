# risk_manager.py

def calculate_position_size(balance, risk_percent, entry, stoploss):
    """
    Tính khối lượng giao dịch dựa trên số dư & rủi ro cho phép (%)
    """
    if entry <= stoploss:
        risk_per_unit = entry - stoploss
    else:
        risk_per_unit = stoploss - entry

    risk_amount = balance * (risk_percent / 100)
    position_size = round(risk_amount / abs(risk_per_unit), 2)
    return position_size
