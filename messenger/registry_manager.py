import json
import os

USER_STATUS_FILE = "data/user_status.json"

# ✅ Tải dữ liệu từ file JSON
def load_data():
    if not os.path.exists(USER_STATUS_FILE):
        return {}
    with open(USER_STATUS_FILE, "r") as f:
        return json.load(f)

# ✅ Lưu dữ liệu trở lại file JSON
def save_data(data):
    with open(USER_STATUS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ✅ Đăng ký người dùng mới
def register_user(user_id, user_name):
    data = load_data()
    if user_id not in data:
        data[user_id] = {
            "name": user_name,
            "approved": False,
            "signal_active": False
        }
        save_data(data)

# ✅ Lấy trạng thái của một người dùng
def get_user_status(user_id):
    return load_data().get(user_id)

# ✅ Cập nhật một trường trong dữ liệu người dùng
def update_user_status(user_id, key, value):
    data = load_data()
    if user_id in data:
        data[user_id][key] = value
        save_data(data)

# ✅ Xét duyệt người dùng → bật nhận tín hiệu
def approve_user(user_id):
    update_user_status(user_id, "approved", True)
    update_user_status(user_id, "signal_active", True)

# ✅ Tắt tín hiệu tạm thời
def deactivate_signal(user_id):
    update_user_status(user_id, "signal_active", False)

# ✅ Bật lại tín hiệu
def activate_signal(user_id):
    update_user_status(user_id, "signal_active", True)

# ✅ Tải toàn bộ danh sách người dùng
def load_user_status():
    return load_data()

# ✅ Kiểm tra xem user có đủ điều kiện nhận tín hiệu không
def is_approved_and_active(user_id):
    status = get_user_status(user_id)
    if not status:
        return False
    return status.get("approved") is True and status.get("signal_active") is True
