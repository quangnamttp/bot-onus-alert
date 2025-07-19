from messenger.message_sender import send_message
from messenger.registry_manager import get_all_registered_users
from config import BOT_CONFIG
from market.price_fetcher import get_onus_price
from macro.event_calendar import get_today_events

def send_morning_brief():
    users = get_all_registered_users()
    price_usdt = get_onus_price("USDT")
    price_btc = get_onus_price("BTC")
    price_eth = get_onus_price("ETH")
    events = get_today_events()

    message = f"""🌞 Chào buổi sáng từ Cofure!

💱 Tỷ giá ONUS hôm nay:
- USDT: {price_usdt:,} VND
- BTC: {price_btc:,} VND
- ETH: {price_eth:,} VND

📅 Lịch tin tức vĩ mô hôm nay:
{events or "Không có tin tức đáng chú ý."}

📈 Nhận định sơ bộ:
- BTC đang trong vùng {analyze_btc(price_btc)}
- Chiến thuật hôm nay: {BOT_CONFIG["strategy"].capitalize()}
    
⏰ Lệnh đầu tiên sẽ gửi lúc 06:15 — chuẩn bị nhé!
"""

    for psid in users:
        send_message(psid, message)

def analyze_btc(price_vnd):
    if price_vnd > 1_500_000_000:
        return "áp lực chốt lời tăng dần"
    elif price_vnd < 1_200_000_000:
        return "vùng hấp dẫn cho vào lệnh Long"
    else:
        return "vùng dao động nhẹ, ưu tiên Limit Entry"
