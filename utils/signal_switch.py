import os

SWITCH_FILE = "signal_status.txt"

def is_signal_enabled():
    """Kiểm tra radar đang bật hay tắt."""
    if not os.path.exists(SWITCH_FILE):
        return True  # Mặc định bật nếu chưa có file
    with open(SWITCH_FILE, "r") as f:
        status = f.read().strip().lower()
        return status == "on"

def toggle_signal(state: str):
    """Cập nhật trạng thái radar: 'on' hoặc 'off'."""
    if state not in ["on", "off"]:
        return
    with open(SWITCH_FILE, "w") as f:
        f.write(state)
