from mess_handler import send_message
from report.end_day_report import generate_report

def send_summary():
    msg = generate_report()
    send_message(msg)
