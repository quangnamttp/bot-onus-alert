import random

def analyze_news_impact(news_title):
    # Mô phỏng dữ liệu thị trường sau khi tin ra → thay bằng real-time fetch nếu cần
    impact = {}

    impact["CPI"] = {
        "actual": 3.1,
        "forecast": 3.3,
        "previous": 3.4,
        "funding_btc": "+0.04%",
        "volume_eth": "vừa bật 28 tỷ VNĐ",
        "reaction": "tích cực"
    }

    impact["FOMC"] = {
        "actual_rate": "Giữ nguyên 5.25%",
        "expectation": "Tăng lên 5.50%",
        "funding_btc": "-0.01%",
        "volume_eth": "sideway",
        "reaction": "đi ngang"
    }

    return impact.get(news_title, {})
