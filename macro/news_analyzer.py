from macro.event_calendar import get_today_events
from macro.macro_tags import tag_event

def analyze_today_news():
    events = get_today_events()
    if not events:
        return None

    alerts = []
    for line in events.splitlines():
        tag = tag_event(line)
        alerts.append(f"{tag} | {line}")

    return "\n".join(alerts)
