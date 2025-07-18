import json

def read_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Lỗi đọc file {path}:", e)
        return []

def write_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"❌ Lỗi ghi file {path}:", e)
