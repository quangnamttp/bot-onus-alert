# config.py

# ✅ Sàn mặc định khi khởi động bot
DEFAULT_EXCHANGE = "Onus"

# ✅ Coin mặc định nếu người dùng chưa chọn
DEFAULT_COIN = "SOL"

# ✅ Tỷ giá quy đổi USD → VNĐ (có thể cập nhật theo ngày)
USD_TO_VND = 24350

# ✅ Danh sách các sàn được hỗ trợ
SUPPORTED_EXCHANGES = [
    "Binance",
    "OKX",
    "MEXC",
    "Nami",
    "Onus",
    "Bybit"
]

# ✅ Danh sách các mã coin bị chặn (token đòn bẩy, mã lỗi)
BLOCKED_COINS = [
    "BTCUP",
    "BTCDOWN",
    "ETH3L",
    "ETH3S",
    "DOGE5L",
    "SHIB1000"
]

# ✅ Mốc giờ lập lịch để gửi bản tin theo chiến thuật phiên
SCHEDULE_TIMES = {
    "morning_brief": "06:00",
    "economic_calendar": "07:00",
    "signal_generator": ["00", "15", "30", "45"],
    "event_watcher": "19:30",
    "night_summary": "22:00"
}

# ✅ URL dự kiến để quét lịch kinh tế (nếu dùng web scraping)
FOREXFACTORY_URL = "https://www.forexfactory.com/calendar"
