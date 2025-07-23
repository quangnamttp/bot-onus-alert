def format(vnd_amount):
    try:
        amount = int(str(vnd_amount).replace(",", ""))
        return "{:,} VNĐ".format(amount)
    except:
        return f"{vnd_amount} VNĐ"
