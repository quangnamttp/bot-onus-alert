import json

def get_admin_psid():
    with open("data/admin_config.json", "r") as f:
        return json.load(f)["admin_psid"]
