import os

SWITCH_FILE = "signal_status.txt"

def is_signal_enabled():
    if not os.path.exists(SWITCH_FILE):
        return True  # mặc định bật
    with open(SWITCH_FILE, "r") as f:
        return f.read().strip() == "on"

def toggle_signal(state: str):
    with open(SWITCH_FILE, "w") as f:
        f.write("on" if state == "on" else "off")
