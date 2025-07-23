# cofure_bot/utils/config_loader.py

import os
from dotenv import load_dotenv

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
MY_USER_ID = os.getenv("MY_USER_ID")
PORT = int(os.getenv("PORT", "5000"))
