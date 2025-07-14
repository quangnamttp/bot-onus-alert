# subscribers.py
def get_subscribers(file_path="subscribers.txt"):
    """Trả về danh sách người dùng đã đăng ký (đã like page)"""
    try:
        with open(file_path, "r") as f:
            users = f.read().splitlines()
        return users
    except:
        return []

def add_subscriber(user_id, file_path="subscribers.txt"):
    """Thêm người dùng mới nếu chưa tồn tại"""
    users = get_subscribers(file_path)
    if user_id not in users:
        with open(file_path, "a") as f:
            f.write(f"{user_id}\n")
