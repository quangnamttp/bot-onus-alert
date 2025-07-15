import datetime
from emotion_handler.greeting_bot import send_morning_greeting
from emotion_handler.summary_bot import send_night_summary

def trigger_events():
    now = datetime.datetime.now().strftime("%H:%M")
    if now == "06:00":
        send_morning_greeting()
    elif now == "22:00":
        send_night_summary()

