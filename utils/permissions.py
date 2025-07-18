import json
import os
from config import ADMIN_CONFIG_PATH

def is_admin(psid):
    if not os.path.exists(ADMIN_CONFIG_PATH):
        return False

    try:
        with open(ADMIN_CONFIG_PATH, "r") as f:
            config = json.load(f)
    except Exception:
        return False

    return psid in config.get("admins", [])
