import requests

def fetch_macro_news(date="today", date_range=None):
    try:
        if date_range == "week":
            url = "https://api.forexfactory.ai/v1/week"
        elif date == "tomorrow":
            url = "https://api.forexfactory.ai/v1/tomorrow"
        else:
            url = "https://api.forexfactory.ai/v1/today"

        response = requests.get(url)
        news_data = response.json()

        important_events = []
        for event in news_data.get("events", []):
            if event.get("impact") in ["High", "Medium"]:
                important_events.append({
                    "time": event.get("time"),
                    "title": event.get("title"),
                    "impact": event.get("impact")
                })

        return important_events
    except:
        return []
