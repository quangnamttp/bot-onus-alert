# 📡 Token dùng để gọi Facebook Graph API gửi tin nhắn Messenger
PAGE_ACCESS_TOKEN = "EAAb3sSMj1z4BPObOczyGPguQHKmyH1fuL1vnZCqWxU8cfepjfnLx2ZAP2ZBcAc09twLKC6X3o3J8mOWIVgpLCpdHQMCnnseZBefdCNyabhHI3Y0Fo35Po0ghTKClxx3bsFTkZABPGfNZClrxwwTHlx1PfZBqv2e1wmNMYsvTsoMD4xKVkO1ZBncI15cpnzHqdjO90KthzPLrngZDZD"

# 🔐 Dùng để xác minh webhook khi Facebook gọi GET lần đầu
VERIFY_TOKEN = "peacelayer1"

# 📂 Đường dẫn file dữ liệu bot sử dụng
PENDING_USERS_PATH = "data/pending_users.json"
ADMIN_CONFIG_PATH = "admin_config.json"
USER_REGISTRY_PATH = "data/user_registry.json"

# ⚙️ Cấu hình chiến lược tín hiệu & lọc coin
DEFAULT_COINS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "MATICUSDT", "OPUSDT"]
DEFAULT_EXCHANGE = "onus"
SEND_CHANNEL = "Messenger"
USE_VND_DISPLAY = True
BASE_CURRENCY_FOR_SIGNALS = "VND"
AVAILABLE_STRATEGIES = ["Scalping", "Swing"]
MIN_VOLUME = 100000
VOLATILE_THRESHOLD = 5

# 🧹 Danh sách coin loại bỏ khỏi phân tích
JUNK_COINS = [
    "PEPEUSDT", "1000BONKUSDT", "DOGE3LUSDT", "SHIB3SUSDT",
    "FLOKIUSDT", "TRUMPUSDT", "WIFUSDT", "SPONGEUSDT", "SATSUSDT"
]
