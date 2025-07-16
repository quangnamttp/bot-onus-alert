from entry_generator import generate_trade_entries
from trend_after_news import analyze_news_impact
from utils import send_message
from test_runner import run_full_test

def main():
    print("🚀 Cofure Bot v1.4 khởi động...")
    
    # Gửi tín hiệu giao dịch
    trade_signals = generate_trade_entries()
    for signal in trade_signals:
        send_message(signal)

    # Phân tích xu hướng sau tin tức (nếu có)
    news_analysis = analyze_news_impact()
    if news_analysis:
        send_message(news_analysis)

    # Khởi chạy kiểm thử toàn hệ thống
    run_full_test()

if __name__ == "__main__":
    main()
