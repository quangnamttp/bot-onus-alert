import os
import time
from dotenv import load_dotenv
from zoneinfo import ZoneInfo  # Python ≥ 3.9

# 🔄 Nạp biến môi trường từ .env
load_dotenv()

# 🌐 Messenger & cấu hình hệ thống
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
VERIFY_TOKEN      = os.getenv("VERIFY_TOKEN", "")
MY_USER_ID        = os.getenv("MY_USER_ID", "")
PORT              = int(os.getenv("PORT", "5000"))

# 🕒 Thiết lập múi giờ toàn hệ thống
TIMEZONE = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")
os.environ['TZ'] = TIMEZONE
try:
    time.tzset()  # Hợp với Linux/Render
except AttributeError:
    pass  # Bỏ qua nếu hệ thống không hỗ trợ

TZ = ZoneInfo(TIMEZONE)

# 📅 Định dạng thời gian
DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")

# ✅ In log kiểm tra khi khởi động
print("✅ VERIFY_TOKEN:", VERIFY_TOKEN)
print("📦 PAGE_ACCESS_TOKEN:", PAGE_ACCESS_TOKEN[:10] + "...")  # Ẩn bớt token
print("📩 MY_USER_ID:", MY_USER_ID)
print("🕒 TIMEZONE:", TIMEZONE)
print("📅 DATETIME_FORMAT:", DATETIME_FORMAT)
print("🚪 PORT:", PORT)
