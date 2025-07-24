import os
import time
from dotenv import load_dotenv
from zoneinfo import ZoneInfo  # Dùng zoneinfo có sẵn trong Python ≥3.9

load_dotenv()

# Thông tin Messenger & máy chủ
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN      = os.getenv("VERIFY_TOKEN")
MY_USER_ID        = os.getenv("MY_USER_ID")
PORT              = int(os.getenv("PORT", "5000"))

# Thiết lập múi giờ hệ thống
TIMEZONE = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")
os.environ['TZ'] = TIMEZONE
try:
    time.tzset()
except AttributeError:
    pass  # Windows không hỗ trợ tzset, nhưng Render server thì hỗ trợ

TZ = ZoneInfo(TIMEZONE)

# Định dạng thời gian để dùng chung trong log, bản tin, v.v.
DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")
