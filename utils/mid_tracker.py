import json
import os

PROCESSED_MIDS_PATH = "data/processed_mids.json"

def ensure_mid_file():
    if not os.path.exists(PROCESSED_MIDS_PATH):
        with open(PROCESSED_MIDS_PATH, "w") as f:
            json.dump([], f)

def is_mid_processed(mid):
    ensure_mid_file()
    try:
        with open(PROCESSED_MIDS_PATH, "r") as f:
            processed = json.load(f)
    except Exception:
        processed = []

    return mid in processed

def mark_mid_processed(mid):
    ensure_mid_file()
    try:
        with open(PROCESSED_MIDS_PATH, "r") as f:
            processed = json.load(f)
    except Exception:
        processed = []

    if mid not in processed:
        processed.append(mid)
        with open(PROCESSED_MIDS_PATH, "w") as f:
            json.dump(processed, f, indent=2)
