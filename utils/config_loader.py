# cofure_bot/utils/config_loader.py

import os
import time
from dotenv import load_dotenv
from zoneinfo import ZoneInfo   # Dùng stdlib, không cần cài thêm

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN      = os.getenv("VERIFY_TOKEN")
MY_USER_ID        = os.getenv("MY_USER_ID")
PORT              = int(os.getenv("PORT", "5000"))

# Timezone setting
TIMEZONE = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")
os.environ['TZ'] = TIMEZONE
try:
    time.tzset()    # áp dụng cho schedule.every().day.at()
except AttributeError:
    pass            # Windows không hỗ trợ, nhưng Linux/Render thì ok

# ZoneInfo để log hoặc datetime aware
TZ = ZoneInfo(TIMEZONE)
