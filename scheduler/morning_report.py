# cofure_bot/scheduler/morning_report.py

import logging
from messenger.send_message import send_template_message
from marketdata.futures_tracker import get_price_data

# Ngưỡng % để highlight
ALERT_THRESHOLD = 5.0

def send_morning_report(user_id):
    try:
        data = get_price_data()
        elements = []
        quick_replies = []

        for symbol, info in data.items():
            price = info.get("price")
            prev  = info.get("prev")
            pct   = ((price - prev) / prev * 100) if prev else 0
            arrow = "🔺" if pct > 0 else "🔻" if pct < 0 else "➡️"
            alert = " 🚨" if abs(pct) >= ALERT_THRESHOLD else ""
            title = f"{symbol}: ${price:,.2f} {arrow}{pct:+.2f}%{alert}"
            btn   = {
                "type": "web_url",
                "url": f"https://www.tradingview.com/symbols/{symbol}USD/",
                "title": "📈 Biểu đồ"
            }

            elements.append({
                "title": title,
                "subtitle": f"Hôm qua: ${prev:,.2f}" if prev else "",
                "buttons": [btn]
            })
            quick_replies.append({
                "content_type": "text",
                "title": f"Thêm {symbol}",
                "payload": f"ADD_{symbol}"
            })

        payload = {
            "template_type": "generic",
            "elements": elements
        }

        logging.info("🌞 Gửi báo cáo sáng nâng cấp với Generic Template")
        send_template_message(
            recipient_id=user_id,
            text="Chào buổi sáng Anh Trương!\nDưới đây là giá hiện tại:",
            template_payload=payload,
            quick_replies=quick_replies
        )

    except Exception:
        logging.exception("❌ Lỗi khi gửi báo cáo sáng nâng cấp")
