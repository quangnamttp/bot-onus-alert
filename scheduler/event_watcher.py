from mess_handler import send_message

def check_macro_event():
    msg = (
        "🔔 Lưu ý: hôm nay có tin CPI lúc 19h30 & FOMC lúc 22h00\n"
        "⚡ Biến động mạnh có thể xảy ra → cân nhắc quản lý vốn!"
    )
    send_message(msg)
