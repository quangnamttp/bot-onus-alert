# cofure_bot/macro/forex_factory_fetcher.py

import requests

def fetch_macro_news():
    try:
        response = requests.get("https://api.forexfactory.ai/v1/today")
        news_data = response.json()

        important_events = []
        for event in news_data.get("events", []):
            if event["impact"] in ["High", "Medium"]:
                important_events.append({
                    "time": event["time"],
                    "title": event["title"],
                    "impact": event["impact"]
                })

        return important_events
    except:
        return []
