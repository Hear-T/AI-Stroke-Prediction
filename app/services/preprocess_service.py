import pandas as pd

def build_cdc_stroke_dataframe(form_values):
    """
    Tiền xử lý thành đúng 14 cột mà mô hình XGBoost Kaggle đang chờ đợi.
    """
    input_data = {
        # 1. Các biến số học & Các biến đã được gán nhị phân (0/1) từ trước
        'gender': [1 if form_values['gender'] == "Male" else 0],
        'age': [form_values['age']],
        'hypertension': [1 if form_values['hypertension'] == "Có" else 0],
        'heart_disease': [1 if form_values['heart_disease'] == "Có" else 0],
        'ever_married': [1 if form_values['ever_married'] == "Yes" else 0],
        'Residence_type': [1 if form_values['residence_type'] == "Urban" else 0],
        'avg_glucose_level': [form_values['avg_glucose_level']],
        'bmi': [form_values['bmi']],
        
        # 2. Các biến One-hot Encoding (work_type và smoking_status)
        'work_type_Private': [1 if form_values['work_type'] == "Private" else 0],
        'work_type_Self-employed': [1 if form_values['work_type'] == "Self-employed" else 0],
        'work_type_children': [1 if form_values['work_type'] == "children" else 0],
        
        'smoking_status_formerly smoked': [1 if form_values['smoking_status'] == "formerly smoked" else 0],
        'smoking_status_never smoked': [1 if form_values['smoking_status'] == "never smoked" else 0],
        'smoking_status_smokes': [1 if form_values['smoking_status'] == "smokes" else 0]
    }
    
    return pd.DataFrame(input_data)