# auto_reporter.py

import json
from datetime import datetime

def log_signal(signal_text, coin, exchange):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "coin": coin,
        "exchange": exchange,
        "message": signal_text
    }

    try:
        with open("signal_logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open("signal_logs.json", "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)
