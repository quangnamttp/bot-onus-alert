CURRENT_VERSION = "1.4"

def get_version():
    return CURRENT_VERSION

def check_updates(remote_version):
    if remote_version != CURRENT_VERSION:
        return f"📦 Có bản cập nhật Cofure Bot mới: v{remote_version}"
    return f"✅ Cofure Bot đang ở phiên bản mới nhất: v{CURRENT_VERSION}"
