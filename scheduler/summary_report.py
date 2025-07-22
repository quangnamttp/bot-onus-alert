from data.signal_log import analyze_day_performance
from messages.greeting_format import format_summary_report
from messenger.registry_manager import load_user_status, is_approved_and_active

def send_summary_report():
    report = analyze_day_performance()
    user_data = load_user_status()
    for user_id, info in user_data.items():
        if is_approved_and_active(user_id):
            msg = format_summary_report(info["name"], report)
            send_message(user_id, msg)

def send_message(user_id, message):
    print(f"[summary_report] → {user_id}: {message}")
