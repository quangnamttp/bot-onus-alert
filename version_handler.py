# version_handler.py

def get_bot_version():
    return "Cofure v1.5"

def is_latest_version(current_version):
    return current_version == get_bot_version()
