# volume_tracker.py

def detect_volume_spike(current_volume, average_volume, threshold=2.5):
    """
    Phát hiện volume tăng mạnh so với trung bình
    """
    if average_volume == 0:
        return False
    ratio = current_volume / average_volume
    return ratio >= threshold
