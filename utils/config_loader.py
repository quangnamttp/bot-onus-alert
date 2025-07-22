import os
from dotenv import load_dotenv

load_dotenv()

MESSENGER_TOKEN = os.getenv("MESSENGER_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PORT = os.getenv("PORT", "5000")
APP_URL = os.getenv("APP_URL", "https://localhost")
