import os
import json

def ensure_file(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=4)
            print(f"✅ Created file: {path}")

def run_init():
    ensure_file("data/user_status.json", {})
    ensure_file("data/signal_log.json", {})
    ensure_file("data/news_log.json", {})
    ensure_file("data/coin_list.json", {
        "coins": ["BTC", "ETH", "SOL", "NEO", "CHI", "C98", "MATIC", "DOGE"]
    })
    ensure_file("data/logs.txt", "")

if __name__ == "__main__":
    run_init()
