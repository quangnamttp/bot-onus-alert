BOT_CONFIG = {
    # 🏦 Sàn giao dịch sử dụng
    "exchange": "onus",  # Cố định ONUS, không cho chọn khác

    # 💰 Đơn vị hiển thị giá
    "currency": "VND",  # Hiển thị giá Entry / TP / SL bằng tiền Việt

    # 🧠 Chiến thuật mặc định
    "strategy": "scalping",  # hoặc "swing" nếu bạn muốn mở rộng

    # 📡 Chu kỳ gửi lệnh (tính theo giây)
    "batch_interval": 1800,  # Cứ 30 phút gửi 1 batch gồm 5 lệnh

    # ⚡ Ngưỡng volume để bot gửi lệnh VIP tức thì (không chờ batch)
    "vip_trigger_volume": 5_000_000,  # VND — nếu vượt, gửi Market ngay

    # 🧹 Danh sách coin loại bỏ thủ công
    "blacklist_coins": ["SHIT", "PUMPX", "SCAMZ"],

    # 🚨 Funding lệch tối đa cho phép
    "max_funding_bias": 0.03,  # nếu lệch quá → loại coin

    # 🔐 PSID của admin nhận bản tin riêng (nếu cần)
    "admin_psid": [],  # để trống nếu chưa cần gửi riêng cho ai

    # 🔊 Mức độ log hiển thị (nếu bot có ghi log)
    "log_level": "info"  # hoặc "debug" khi test, "error" khi deploy
}
