---
title: AI Stroke Prediction
emoji: 🏥
colorFrom: red
colorTo: pink
sdk: docker
pinned: false
app_port: 7860
---

# 🏥 AI Stroke Prediction System

AI Stroke Prediction System là hệ thống hỗ trợ **dự đoán nguy cơ đột quỵ** dựa trên dữ liệu sức khỏe cá nhân theo hướng **CDC/BRFSS**.

> **Lưu ý:** Hệ thống chỉ phục vụ mục đích học tập, nghiên cứu và tham khảo. Kết quả dự đoán không thay thế chẩn đoán hoặc tư vấn trực tiếp từ bác sĩ.

---

## 🎯 Mục tiêu dự án

Dự án được xây dựng nhằm:

- Thu thập thông tin sức khỏe cơ bản từ người dùng qua giao diện web
- Ước tính nguy cơ đột quỵ bằng mô hình AI
- Hiển thị kết quả dự đoán dưới dạng phần trăm nguy cơ
- Đưa ra lời khuyên cá nhân hóa dựa trên hồ sơ sức khỏe
- Minh họa việc ứng dụng AI vào bài toán y tế dự phòng

---

## ⭐ Tính năng chính

- Giao diện nhập thông tin sức khỏe trực quan bằng Streamlit
- Dự đoán nguy cơ đột quỵ từ dữ liệu người dùng nhập vào
- Hiển thị mức nguy cơ bằng biểu đồ gauge
- Phân loại nguy cơ thành 3 mức: thấp, trung bình, cao
- Sinh lời khuyên cá nhân hóa theo hồ sơ người dùng
- Có thể test nhanh mô hình bằng script mẫu
- Có thể train lại mô hình nếu cần

---

## 💻 Công nghệ sử dụng

### ⚙️ Backend / Xử lý
- Python
- Pandas

### 🎨 Giao diện
- Streamlit
- Plotly

### 🧠 AI / Machine Learning
- XGBoost
- Dữ liệu theo hướng CDC/BRFSS

### 🛠️ Công cụ hỗ trợ
- Git / GitHub

---

## 🏗️ Kiến trúc hệ thống

```text
Người dùng nhập dữ liệu sức khỏe
            |
            v
Giao diện Streamlit
            |
            v
Tiền xử lý dữ liệu đầu vào
            |
            v
Mô hình XGBoost dự đoán nguy cơ đột quỵ
            |
            v
Hiển thị phần trăm nguy cơ + mức cảnh báo
            |
            v
Sinh lời khuyên cá nhân hóa
```

---

## 📁 Cấu trúc thư mục chính

```text
AI-Stroke-Prediction-test/
│
├── app/
│   ├── config.py
│   ├── models_ai/
│   │   └── cdc_stroke_model.py
│   ├── services/
│   │   ├── advice_service.py
│   │   ├── chart_service.py
│   │   ├── prediction_service.py
│   │   └── preprocess_service.py
│   ├── ui/
│   │   └── stroke_cdc_page.py
│   └── utils/
│       └── translations.py
│
├── data/
│   └── raw/
│
├── scripts/
│   ├── test_predict.py
│   └── train_cdc_model_fixed.py
│
├── trained_models/
│   └── xgboost_cdc_stroke_model.pkl
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## 🔄 Luồng hoạt động

1. Người dùng nhập thông tin sức khỏe trên giao diện
2. Hệ thống gom dữ liệu thành `form_values`
3. Module tiền xử lý chuyển dữ liệu về đúng dạng mô hình yêu cầu
4. Mô hình AI dự đoán xác suất nguy cơ đột quỵ
5. Hệ thống hiển thị:
   - phần trăm nguy cơ
   - mức cảnh báo
   - lời khuyên cá nhân hóa

---

## 🚨 Các mức đánh giá nguy cơ

Hệ thống hiện chia kết quả dự đoán thành 3 mức:

- **Nguy cơ thấp**
- **Nguy cơ trung bình**
- **Nguy cơ cao**

Mức phân loại này được xây dựng dựa trên xác suất do mô hình trả về.

---

## 🚀 Cách chạy local

**1. Clone project**
```bash
git clone https://github.com/Hear-T/AI-Stroke-Prediction.git
cd AI-Stroke-Prediction-test
```

**2. Tạo môi trường ảo**
```bash
python -m venv .venv
```

**3. Kích hoạt môi trường ảo**

Trên Windows:
```bash
.venv\Scripts\activate
```

Trên macOS / Linux:
```bash
source .venv/bin/activate
```

**4. Cài thư viện**
```bash
pip install -r requirements.txt
```

**5. Chạy ứng dụng**
```bash
streamlit run streamlit_app.py
```

Sau khi chạy, Streamlit sẽ cung cấp đường dẫn local để mở trên trình duyệt.

---

## 🔌 Thành phần chính của hệ thống

- `streamlit_app.py` — file chạy chính của ứng dụng
- `app/ui/stroke_cdc_page.py` — giao diện nhập liệu và hiển thị kết quả
- `app/services/preprocess_service.py` — xử lý dữ liệu đầu vào
- `app/services/prediction_service.py` — tính xác suất và phân loại nguy cơ
- `app/services/chart_service.py` — tạo biểu đồ kết quả
- `app/services/advice_service.py` — sinh lời khuyên cá nhân hóa
- `app/models_ai/cdc_stroke_model.py` — nạp mô hình đã huấn luyện
- `scripts/test_predict.py` — test nhanh mô hình
- `scripts/train_cdc_model_fixed.py` — train lại mô hình nếu cần

---

## 🧪 Cách test nhanh mô hình

Chạy lệnh sau:

```bash
python scripts/test_predict.py
```

Script này sẽ nạp mô hình CDC, tạo một bộ dữ liệu mẫu và in ra xác suất nguy cơ dự đoán.

---

## 📈 Trạng thái hiện tại của dự án

Đây là phiên bản có thể demo được.

Hệ thống hiện đang sử dụng:
- Mô hình XGBoost đã train sẵn
- Giao diện Streamlit
- Dữ liệu đầu vào theo hướng CDC/BRFSS
- Logic lời khuyên dựa trên hồ sơ người dùng

Các phần có thể mở rộng thêm trong tương lai:
- Tối ưu mô hình để tăng độ chính xác
- Bổ sung đánh giá mô hình bằng các chỉ số như Accuracy, Precision, Recall, F1-score
- Triển khai online
- Cải thiện giao diện người dùng
- Bổ sung lưu lịch sử dự đoán

---

## ⚠️ Lưu ý an toàn

Hệ thống này chỉ hỗ trợ dự đoán nguy cơ ban đầu và cung cấp thông tin tham khảo.
Kết quả từ hệ thống không thay thế chẩn đoán, chỉ định điều trị hoặc tư vấn trực tiếp từ bác sĩ.

---

## 👨‍💻 Thông tin sinh viên thực hiện

Bạn có thể chỉnh lại phần này theo thông tin của mình:

- **Họ tên:** ...
- **MSSV:** ...
- **Lớp:** ...
- **Khoa / Ngành:** ...
- **Giảng viên hướng dẫn:** ...
- **Tên đề tài:** AI Stroke Prediction System
