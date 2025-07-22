import time

last_sent = {}

def can_send(user_id, delay=30):
    now = time.time()
    if user_id not in last_sent or now - last_sent[user_id] > delay:
        last_sent[user_id] = now
        return True
    return False
