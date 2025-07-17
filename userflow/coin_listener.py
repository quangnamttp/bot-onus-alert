import json

def get_user_coins(psid):
    try:
        with open("user_config.json") as f:
            config = json.load(f)
        return config.get(psid, {}).get("coins", ["BTCUSDT", "ETHUSDT"])
    except:
        return ["BTCUSDT", "ETHUSDT"]

def set_user_coins(psid, coins):
    try:
        with open("user_config.json") as f:
            config = json.load(f)
    except:
        config = {}
    if psid not in config:
        config[psid] = {}
    config[psid]["coins"] = coins
    with open("user_config.json", "w") as f:
        json.dump(config, f, indent=2)
