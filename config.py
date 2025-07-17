# ✅ Danh sách coin mặc định theo dõi
DEFAULT_COINS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT",
    "MATICUSDT", "OPUSDT"
]

# ✅ Sàn mặc định nếu người dùng chưa chọn
DEFAULT_EXCHANGE = "onus"

# ✅ Kênh gửi tín hiệu qua Messenger Fanpage
SEND_CHANNEL = "Messenger"

# ✅ Toàn bộ giá sẽ xử lý bằng đơn vị VND
USE_VND_DISPLAY = True            # giá hiển thị là VND
BASE_CURRENCY_FOR_SIGNALS = "VND"  # giá phân tích, tính toán lệnh

# ✅ Chiến thuật phân loại tín hiệu
AVAILABLE_STRATEGIES = ["Scalping", "Swing"]

# ✅ Ngưỡng volume tối thiểu để bỏ coin yếu
MIN_VOLUME = 100000

# ✅ Biến động đủ mạnh để xét tạo lệnh mới
VOLATILE_THRESHOLD = 5  # ±5% hoặc hơn

# ✅ Danh sách coin rác loại trừ triệt để
JUNK_COINS = [
    "PEPEUSDT", "1000BONKUSDT", "DOGE3LUSDT",
    "SHIB3SUSDT", "FLOKIUSDT", "TRUMPUSDT",
    "WIFUSDT", "SPONGEUSDT", "SATSUSDT"
]
