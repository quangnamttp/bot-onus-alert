# main.py

from userflow.exchange_selector import ExchangeSelector
from userflow.coin_listener import CoinListener

def start_bot():
    print("🚀 Cofure Bot khởi động...")
    exchange = ExchangeSelector()
    coin = CoinListener()

    print(f"🟢 Sàn mặc định: {exchange.get_current_exchange()}")
    print("📌 Bot đang đợi người dùng chọn coin để phân tích...")

    # Ví dụ nhập coin & sàn từ người dùng
    user_san = input("Bạn chọn sàn nào? ").strip()
    print(exchange.update_exchange(user_san))
    
    user_coin = input("Bạn muốn phân tích coin nào? ").strip()
    print(coin.update_coin(user_coin))

    print(f"🔎 Phân tích đang chuẩn bị cho: Coin {coin.get_current_coin()} trên sàn {exchange.get_current_exchange()}")

if __name__ == "__main__":
    start_bot()
