# AI Stroke Prediction - CDC Only

## Mục tiêu của bản này

- Mở ứng dụng là vào thẳng form dự đoán CDC
- Bỏ sidebar điều hướng và các module không còn dùng
- Dọn bớt file, thư mục và model dư thừa để project gọn hơn
- Giữ lại phần cần thiết để tiếp tục train, test và demo mô hình CDC

## Cấu trúc chính

```text
AI-Stroke-Prediction-test/
├── app/
│   ├── config.py
│   ├── models_ai/
│   ├── services/
│   ├── ui/
│   └── utils/
├── data/
│   └── raw/
├── notebooks/
│   └── ai_cdc_brfss.ipynb
├── scripts/
│   ├── test_predict.py
│   └── train_cdc_model_fixed.py
├── trained_models/
│   └── xgboost_cdc_stroke_model.pkl
├── streamlit_app.py
└── requirements.txt
```

## Chạy project

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Model đang dùng

- File model chính: `trained_models/xgboost_cdc_stroke_model.pkl`
- Dữ liệu nền: CDC/BRFSS
- Giao diện hiện chỉ phục vụ module CDC

## Ghi chú

- Mô hình hiện đang xử lý biến hút thuốc theo hướng **có hút hiện tại / không hút hiện tại**.
- File `scripts/test_predict.py` dùng để test nhanh đầu ra của model CDC.
- File `scripts/train_cdc_model_fixed.py` được giữ lại để bạn có thể train lại model sau này.
