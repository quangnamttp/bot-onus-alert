# cofure_bot/utils/config_loader.py

import os
import time
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()

# Thông tin Messenger & máy chủ
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN      = os.getenv("VERIFY_TOKEN")
MY_USER_ID        = os.getenv("MY_USER_ID")
PORT              = int(os.getenv("PORT", "5000"))

# Thiết lập múi giờ ứng dụng
# - TIMEZONE: tên timezone theo tz database (vd: Asia/Ho_Chi_Minh)
# - TZ: dùng cho time.tzset() để schedule.every().day.at() chạy đúng localtime
TIMEZONE = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")
os.environ['TZ'] = TIMEZONE
try:
    time.tzset()
except AttributeError:
    # time.tzset() không hỗ trợ trên Windows
    pass

# Đối tượng pytz để log hoặc xử lý datetime có timezone
TZ = timezone(TIMEZONE)
