# cofure_bot/messages/greeting_format.py

from utils.vnd_formatter import format_vnd

def morning_greeting(name, btc, eth, sol):
    btc_vnd = format_vnd(btc)
    eth_vnd = format_vnd(eth)
    sol_vnd = format_vnd(sol)

    return f"""
🌞 Chào buổi sáng nha {name} ☀️  
📈 Giá mở phiên hôm nay:

• BTC: {btc_vnd}  
• ETH: {eth_vnd}  
• SOL: {sol_vnd}

📬 Cofure đã sẵn sàng bắt sóng phiên mới rồi 😎  
Chúc bạn một ngày trade thật thành công nhé!
""".strip()
