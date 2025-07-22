from datetime import datetime

def log(content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("data/logs.txt", "a") as f:
        f.write(f"[{timestamp}] {content}\n")
