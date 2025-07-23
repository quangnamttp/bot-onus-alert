# cofure_bot/utils/vnd_formatter.py

def format_vnd(amount):
    try:
        if isinstance(amount, str):
            amount = float(amount.replace(",", "").replace(".", ""))
        formatted = f"{int(amount):,}".replace(",", ".")
        return f"{formatted} VNĐ"
    except:
        return f"{amount} VNĐ"
