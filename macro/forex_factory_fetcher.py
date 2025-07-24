import requests

# 🔎 Từ khoá nhạy cảm với crypto market
CRYPTO_KEYWORDS = [
    "Powell", "FOMC", "CPI", "inflation", "interest rate", "Nonfarm",
    "Lagarde", "PCE", "employment", "Fed", "rate hike", "monetary policy",
    "hawkish", "dovish", "volatility", "liquidity", "yield curve"
]

def is_crypto_relevant(event):
    title = event.get("title", "").lower()
    impact = event.get("impact", "").strip()
    
    # ✅ Lọc theo impact hoặc có từ khóa trong tiêu đề
    return (
        impact in ["High", "Medium"] or
        any(keyword.lower() in title for keyword in CRYPTO_KEYWORDS)
    )

def fetch_macro_news(date="today", date_range=None):
    try:
        # 🌐 Chọn API endpoint theo ngày yêu cầu
        if date_range == "week":
            url = "https://api.forexfactory.ai/v1/week"
        elif date == "tomorrow":
            url = "https://api.forexfactory.ai/v1/tomorrow"
        else:
            url = "https://api.forexfactory.ai/v1/today"

        response = requests.get(url)
        news_data = response.json()

        # 🎯 Lọc tin tức quan trọng
        important_events = []
        for event in news_data.get("events", []):
            if is_crypto_relevant(event):
                important_events.append({
                    "time": event.get("time", "⏰"),
                    "title": event.get("title", "Không rõ tiêu đề"),
                    "impact": event.get("impact", "Unknown")
                })

        return important_events

    except Exception as e:
        print(f"[Lỗi fetch macro]: {e}")
        return []
