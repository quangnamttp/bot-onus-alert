import json

def get_exchange(psid):
    try:
        with open("user_config.json") as f:
            config = json.load(f)
        return config.get(psid, {}).get("exchange", "onus")
    except:
        return "onus"

def set_exchange(psid, exchange):
    try:
        with open("user_config.json") as f:
            config = json.load(f)
    except:
        config = {}
    if psid not in config:
        config[psid] = {}
    config[psid]["exchange"] = exchange
    with open("user_config.json", "w") as f:
        json.dump(config, f, indent=2)
