# 🤖 Cofure Bot v1.5

Bot gửi tín hiệu Futures qua Messenger: phân tích volume, RSI, funding, lịch vĩ mô.  
Bản tin sáng — tín hiệu lệnh — báo cáo tối — phản ứng tức thì khi có tin CPI/FOMC.

## Cài đặt
1. Cài thư viện: `pip install -r requirements.txt`
2. Tạo file `.env` từ `.env.example` và điền token Messenger
3. Chạy bot: `python main.py`

## Cấu trúc chính
- `core/`: phân tích chiến thuật kỹ thuật
- `scheduler/`: bản tin theo lịch
- `marketdata/`: chỉ báo & dữ liệu thị trường
- `userflow/`: thông tin coin người dùng chọn
- `report/`: thống kê hiệu suất
- `messages/`: format tin nhắn & emoji
