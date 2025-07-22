from marketdata.volume_scanner import get_accumulating_coins
from marketdata.spread_monitor import check_pinbar_rsi

def detect_pre_breakout():
    coins = get_accumulating_coins()
    setups = []

    for coin in coins:
        rsi_info = check_pinbar_rsi(coin)
        if rsi_info["rsi"] in range(55, 65) and rsi_info["pinbar"]:

            setups.append({
                "coin": coin,
                "entry_hint": rsi_info["entry"],
                "reason": f"Đang tích lũy: volume đều, funding nghiêng {rsi_info['bias']}, mô hình pinbar tại vùng RSI {rsi_info['rsi']}",
                "suggest": "Có thể vào sớm trước khi giá bung mạnh."
            })

    return setups
