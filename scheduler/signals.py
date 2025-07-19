from messenger.message_sender import send_message
from messenger.registry_manager import get_all_registered_users
from config import BOT_CONFIG
from core.coin_filter import get_filtered_coins
from core.signal_generator import generate_signals
from market.price_fetcher import get_onus_price

def send_batch_signals():
    users = get_all_registered_users()
    coins = get_filtered_coins()
    signals = generate_signals(coins)

    for signal in signals:
        entry = get_onus_price(signal["coin"])
        msg = f"""📡 Tín hiệu Cofure ({BOT_CONFIG['strategy'].upper()})

🪙 Coin: {signal['coin']}
🎯 Entry: {entry:,} VND
📈 TP: {signal['tp']:,} VND
📉 SL: {signal['sl']:,} VND
🧮 R:R = {signal['rr']}

⏳ {signal['tag']} | Sàn: ONUS
"""
        for psid in users:
            send_message(psid, msg)
