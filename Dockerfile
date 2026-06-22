# 1. Sử dụng môi trường Python 3.10 siêu nhẹ
FROM python:3.10-slim

# 2. Thiết lập thư mục làm việc trong máy ảo
WORKDIR /code

# 3. Cài đặt các công cụ hệ thống cơ bản để build thư viện (nếu cần)
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy file requirements và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ mã nguồn của bạn vào máy ảo
COPY . .

# 6. Mở cổng 7860 (Quy định bắt buộc của Hugging Face)
EXPOSE 7860

# 7. Lệnh khởi động Streamlit khi bật máy ảo
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.address=0.0.0.0"]