import os, json

def ensure_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)

def init_bot_files():
    ensure_file("data/user_registry.json")
    ensure_file("data/processed_mids.json")
